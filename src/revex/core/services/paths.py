"""
Filesystem locations.

Centralizes application paths and directory
layout definitions.

Responsible for:
    - defining application directories
    - providing canonical filesystem paths

Not responsible for:
    - filesystem operations
    - directory creation
"""

from pathlib import Path


def find_project_root() -> Path:
    """Traverses upward from the current working directory to locate the project root"""
    current = Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        # The project root is identified by our build file or the canonical manifest
        if (parent / "pyproject.toml").exists() or (
            parent / "content/manifest.json"
        ).exists():
            return parent
    return current  # fallback to cwd if not found


PROJECT_ROOT = find_project_root()
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
STATE_DIR = PROJECT_ROOT / ".user_data"
CONTENT_DIR = PROJECT_ROOT / "content"
