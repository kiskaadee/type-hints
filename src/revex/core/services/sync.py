"""
Workspace synchronization.

Keeps the learner workspace aligned with
the bundled course content.

Responsible for:
    - detecting missing exercises
    - copying new exercises into workspace
    - updating workspace metadata

Guarantees:
    - learner work is never overwritten

Not responsible for:
    - validation
    - progress tracking
    - content discovery
"""

from pydantic import BaseModel, Field

from revex.core.services.config import load_config
from revex.core.services.content import (
    get_exercise_name,
    load_exercise_template,
    load_problem_description,
)
from revex.core.services.manifest import list_manifest_exercises
from revex.core.services.paths import WORKSPACE_DIR


class SyncRecord(BaseModel):
    exercise_id: str
    exercise_name: str
    status: str  # "added" | "skipped" | "failed"
    reason: str | None = None


class SyncSummary(BaseModel):
    records: list[SyncRecord] = Field(default_factory=list)
    added_count: int = 0
    skipped_count: int = 0
    failed_count: int = 0


def sync_workspace() -> SyncSummary:
    """
    Synchronizes learner workspace with the latest course content.
    1. Loads manifest.
    2. Loads active config (for language settings).
    3. For each exercise:
       - Determines destination path: workspace/<group>/<padded_id>-<exercise_name>/
       - Checks if <exercise_name>.py already exists (if so, skips to protect learner work).
       - Copies exercise.pytxt to <exercise_name>.py
       - Copies problem.<lang>.md to README.md
    4. Compiles and returns SyncSummary.
    """
    summary = SyncSummary()

    try:
        config = load_config()
        lang = config.settings.language
    except Exception:
        lang = "en"  # fallback if config is corrupt

    try:
        exercises = list_manifest_exercises()
    except Exception as e:
        # If the manifest itself fails to load, we raise it
        raise e

    for exercise in exercises:
        exercise_name = get_exercise_name(exercise)
        dest_dir = WORKSPACE_DIR / exercise.group / f"{exercise.id}-{exercise_name}"
        dest_py_path = dest_dir / f"{exercise_name}.py"
        dest_readme_path = dest_dir / "README.md"

        if dest_py_path.exists():
            summary.records.append(
                SyncRecord(
                    exercise_id=exercise.id,
                    exercise_name=exercise_name,
                    status="skipped",
                    reason="already exists",
                )
            )
            summary.skipped_count += 1
            continue

        try:
            # Create target workspace folder
            dest_dir.mkdir(parents=True, exist_ok=True)

            # Write template file
            template = load_exercise_template(exercise)
            dest_py_path.write_text(template, encoding="utf-8")

            # Write problem sheet README
            readme = load_problem_description(exercise, lang=lang)
            dest_readme_path.write_text(readme, encoding="utf-8")

            summary.records.append(
                SyncRecord(
                    exercise_id=exercise.id,
                    exercise_name=exercise_name,
                    status="added",
                )
            )
            summary.added_count += 1
        except Exception as e:
            summary.records.append(
                SyncRecord(
                    exercise_id=exercise.id,
                    exercise_name=exercise_name,
                    status="failed",
                    reason=str(e),
                )
            )
            summary.failed_count += 1

    return summary
