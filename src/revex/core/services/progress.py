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
from datetime import datetime, timezone
from pathlib import Path

from revex.core.models import ExerciseProgress, Progress, ProgressError
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
    except json.JSONDecodeError as e:
        raise ProgressError(f"Syntax error in progress file: {e}") from e
    except Exception as e:
        raise ProgressError(f"Invalid progress data: {e}") from e


def save_progress(progress: Progress) -> None:
    """Saves the progress model to progress.json."""
    _ = PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _ = PROGRESS_PATH.write_text(progress.model_dump_json(indent=4), encoding="utf-8")


def record_attempt(exercise_id: str, completed: bool) -> None:
    """Increments attempt count and sets completion status/timestamp in progress.json."""
    progress = load_progress()

    if exercise_id not in progress.completed_exercises:
        progress.completed_exercises[exercise_id] = ExerciseProgress(
            completed=False,
            attempts=0,
        )

    ex_progress = progress.completed_exercises[exercise_id]
    ex_progress.attempts += 1

    if completed:
        ex_progress.completed = True
        ex_progress.completed_at = datetime.now(timezone.utc)

    save_progress(progress)


def get_progress_statistics() -> dict[str, dict[str, int]]:
    """
    Calculates module-by-module (group) completion statistics and overall totals.

    Returns:
        A dictionary mapping group names (plus a special 'overall' key) to a dict containing:
        - 'completed': number of completed exercises
        - 'total': total number of exercises in the group
        - 'attempts': total attempts within the group
    """
    from revex.core.services.manifest import list_manifest_exercises

    progress = load_progress()
    exercises = list_manifest_exercises()

    stats: dict[str, dict[str, int]] = {}
    overall = {"completed": 0, "total": 0, "attempts": 0}

    for ex in exercises:
        group = ex.group
        if group not in stats:
            stats[group] = {"completed": 0, "total": 0, "attempts": 0}

        ex_progress = progress.completed_exercises.get(ex.id)
        is_completed = False
        attempts = 0
        if ex_progress:
            is_completed = ex_progress.completed
            attempts = ex_progress.attempts

        stats[group]["total"] += 1
        overall["total"] += 1

        stats[group]["attempts"] += attempts
        overall["attempts"] += attempts

        if is_completed:
            stats[group]["completed"] += 1
            overall["completed"] += 1

    stats["overall"] = overall
    return stats
