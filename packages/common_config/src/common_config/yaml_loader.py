"""Production-safe YAML configuration loader with environment overlay merging.

This module implements the layered config strategy used across all services:

    base.yaml  →  {environment}.yaml  (deep-merged)  →  env vars (highest priority)

The deep-merge ensures nested dicts (like ``hyperparameters:``) are *overlaid*,
not wholesale-replaced — a common pitfall with naive ``dict.update()``.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

from common_exceptions.infrastructure_exceptions import ConfigurationError


# ── Public API ───────────────────────────────────────────────────────────

def load_yaml_config(
    config_dir: Path | str,
    environment: str = "local",
) -> dict[str, Any]:
    """Load and merge YAML configuration files for the given environment.

    Resolution order (last wins for overlapping keys):
        1. ``config_dir/base.yaml``   — required, contains all defaults
        2. ``config_dir/{environment}.yaml`` — optional environment overlay

    Args:
        config_dir: Absolute or relative path to the directory containing
            ``base.yaml`` and optional overlay files.
        environment: The target environment name (e.g. ``"local"``,
            ``"staging"``, ``"production"``).

    Returns:
        A fully-merged configuration dictionary.

    Raises:
        ConfigurationError: If ``base.yaml`` is missing or contains
            invalid YAML syntax.
    """
    config_dir = Path(config_dir)

    # 1. Load the mandatory base file
    base_path = config_dir / "base.yaml"
    base_config = _read_yaml(base_path, required=True)

    # 2. Optionally overlay the environment-specific file
    overlay_path = config_dir / f"{environment}.yaml"
    if overlay_path.exists():
        overlay_config = _read_yaml(overlay_path, required=False)
        base_config = deep_merge(base_config, overlay_config)

    return base_config


# ── Deep Merge ───────────────────────────────────────────────────────────

def deep_merge(
    base: dict[str, Any],
    overlay: dict[str, Any],
) -> dict[str, Any]:
    """Recursively merge *overlay* into a **copy** of *base*.

    - Dict values are merged recursively (not replaced).
    - All other types in the overlay overwrite the base value.
    - Neither input dict is mutated.

    Example::

        >>> deep_merge(
        ...     {"model": {"n_estimators": 100, "lr": 0.1}},
        ...     {"model": {"n_estimators": 500}},
        ... )
        {'model': {'n_estimators': 500, 'lr': 0.1}}
    """
    merged = copy.deepcopy(base)

    for key, overlay_value in overlay.items():
        base_value = merged.get(key)

        if isinstance(base_value, dict) and isinstance(overlay_value, dict):
            merged[key] = deep_merge(base_value, overlay_value)
        else:
            merged[key] = copy.deepcopy(overlay_value)

    return merged


# ── Private helpers ──────────────────────────────────────────────────────

def _read_yaml(path: Path, *, required: bool) -> dict[str, Any]:
    """Read a single YAML file and return its contents as a dict.

    Args:
        path: Path to the YAML file.
        required: If ``True``, raise ``ConfigurationError`` when the
            file does not exist.

    Returns:
        Parsed YAML content, or an empty dict for empty / missing
        optional files.
    """
    if not path.exists():
        if required:
            raise ConfigurationError(
                message=f"Required configuration file not found: {path}",
                details={"path": str(path)},
            )
        return {}

    try:
        text = path.read_text(encoding="utf-8")
        content = yaml.safe_load(text)
        return content if isinstance(content, dict) else {}
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            message=f"Failed to parse YAML file: {path}",
            details={"path": str(path), "parse_error": str(exc)},
        )
