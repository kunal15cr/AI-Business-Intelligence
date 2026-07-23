from pathlib import Path


def generate_tree(
    directory: Path,
    prefix: str = "",
    ignored_dirs=None,
    ignored_files=None,
):
    if ignored_dirs is None:
        ignored_dirs = {
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "node_modules",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
        }

    if ignored_files is None:
        ignored_files = {
            ".DS_Store",
        }

    entries = sorted(
        [
            item
            for item in directory.iterdir()
            if item.name not in ignored_dirs
            and item.name not in ignored_files
        ],
        key=lambda x: (x.is_file(), x.name.lower()),
    )

    lines = []

    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{entry.name}")

        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            lines.extend(
                generate_tree(
                    entry,
                    prefix + extension,
                    ignored_dirs,
                    ignored_files,
                )
            )

    return lines


def save_project_structure(project_path: str, output_file: str = "project_structure.txt"):
    root = Path(project_path)

    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {project_path}")

    tree = [root.name]
    tree.extend(generate_tree(root))

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(tree))

    print(f"\nProject structure saved to '{output_file}'")


if __name__ == "__main__":
    save_project_structure(
        project_path=".",  # Current directory
        output_file="project_structure.txt",
    )