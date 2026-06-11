"""
Progress tracking.

Tracks learner completion state and progress
through the course.

Responsible for:
    - loading progress data
    - saving progress data
    - marking exercises as completed
    - reporting completion statistics

Not responsible for:
    - validating exercises
    - loading exercise content
    - synchronization
"""

import json
from pathlib import Path

from revex.core.models import Progress
from revex.core.services.paths import STATE_DIR

PROGRESS_PATH: Path = STATE_DIR / "progress.json"


def load_progress() -> Progress:
    """Loads and validates the progress.json file."""
    if not PROGRESS_PATH.is_file():
        return Progress()
    try:
        return Progress.model_validate(
            json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
        )
    except Exception:
        return Progress()


def save_progress(progress: Progress) -> None:
    """Saves the progress model to progress.json."""
    _ = PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _ = PROGRESS_PATH.write_text(progress.model_dump_json(indent=4), encoding="utf-8")
