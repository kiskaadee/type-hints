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

WORKSPACE_DIR = Path("workspace")
STATE_DIR = Path(".user_data")
CONTENT_DIR = Path("content")
