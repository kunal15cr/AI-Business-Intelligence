import yaml
import pickle
from pathlib import Path
from typing import Any, Dict

# Import the custom enterprise tools we built
from churn_pipeline.exception.exception import CIPGenericError
from churn_pipeline.logging.logging import get_logger

logger = get_logger(__name__)


def read_yaml(file_path: Path | str) -> Dict[str, Any]:
    """
    Safely reads a YAML file and returns its contents as a dictionary.
    
    Args:
        file_path (Path | str): The absolute or relative path to the YAML file.
        
    Returns:
        Dict[str, Any]: The parsed YAML content.
    """
    path = Path(file_path)

    # 1. Fail Fast: Does the file even exist?
    if not path.exists():
        # Changed to CIPGenericError to support dynamic kwargs like 'attempted_path'
        raise CIPGenericError(
            message=f"YAML configuration file is missing at {path}",
            error_code="YAML_FILE_NOT_FOUND",
            attempted_path=str(path)
        )

    try:
        # 2. Safely read the file enforcing UTF-8 encoding
        with open(path, "r", encoding="utf-8") as f:
            # Always use safe_load, never load() to prevent arbitrary code execution
            content = yaml.safe_load(f)
            
        logger.info("Successfully loaded YAML file", extra={"file_path": str(path)})
        
        # 3. Handle edge case where the YAML file is completely empty
        return content or {}
        
    except yaml.YAMLError as e:
        # 4. Handle syntax/parsing errors (e.g., missing a colon in the YAML)
        logger.error(f"Failed to parse YAML syntax at {path}", exc_info=True)
        # Changed to CIPGenericError to support dynamic kwargs
        raise CIPGenericError(
            message="Failed to parse YAML content. Check syntax formatting.",
            error_code="YAML_PARSE_ERROR",
            attempted_path=str(path),
            original_error=str(e)
        )
    except Exception as e:
        # 5. Catch-All for bizarre OS errors (e.g., file permissions locked)
        logger.critical(f"Unexpected OS error reading YAML file at {path}", exc_info=True)
        raise CIPGenericError(
            message="Unexpected system error while attempting to read YAML file.",
            error_code="UNEXPECTED_IO_ERROR",
            attempted_path=str(path)
        )


def save_artifact(obj: Any, file_path: Path | str) -> None:
    """
    Safely saves a Python object (like an XGBoost model) to disk.
    """
    path = Path(file_path)
    
    try:
        # Automatically create the folder if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "wb") as f:
            pickle.dump(obj, f)
            
        logger.info("Artifact successfully saved", extra={"file_path": str(path)})
        
    except Exception as e:
        logger.error(f"Failed to save artifact to {path}", exc_info=True)
        raise CIPGenericError(
            message="Failed to serialize and save artifact to disk.",
            error_code="ARTIFACT_SAVE_ERROR",
            attempted_path=str(path)
        )