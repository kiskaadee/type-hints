"""
Workspace initialization.

Creates the local learner environment required
to use the application.

Responsible for:
    - creating workspace/
    - creating .user_data/
    - generating default config
    - generating initial progress state

Not responsible for:
    - content updates
    - exercise validation
    - progress reporting
"""

# usage: uv run revex init
# -[✓]  creates workspace/
# -[ ]      Populate Workspace from Manifest: exercise.pytxt exercise.py # to-do
# -[✓]  creates .user_data/
# -[✓]      creates config.toml
# -[✓]      creates progress.json
# -[✓]  creates revex_cache/

from revex.core.models import Progress
from revex.core.services.config import load_config, save_config
from revex.core.services.paths import CACHE_DIR, STATE_DIR, WORKSPACE_DIR
from revex.core.services.progress import PROGRESS_PATH, save_progress


def initialize_environment() -> None:
    """
    Safely checks and creates /workspace, and /.user_data directories,
    and generates the default config.toml and empty progress.json
    logs if they do not exist.
    """
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize config.toml if it does not exist
    config_path = STATE_DIR / "config.toml"
    if not config_path.exists():
        save_config(load_config(default=True))

    # Initialize progress.json if it does not exist
    if not PROGRESS_PATH.exists():
        save_progress(Progress())
