"""
Registry layer.

The manifest is the authoritative catalog of
content available in the current release.

Responsibilities:
    - discover exercises
    - map exercise ids to content locations
    - expose content version information

Not responsible for:
    - loading exercise resources
    - progress tracking
    - validation
    - synchronization
"""

import json
from pathlib import Path

from pydantic import ValidationError

from revex.core.models import (
    ExerciseNotFoundError,
    Manifest,
    ManifestError,
    ManifestExercise,
)
from revex.core.services.constants import MANIFEST_FILENAME
from revex.core.services.paths import CONTENT_DIR

MANIFEST_PATH: Path = CONTENT_DIR / MANIFEST_FILENAME


def load_manifest() -> Manifest:
    """
    Loads and parses content/manifest.json
    Raises a ManifestError if the file is missing or malformed
    """
    if not MANIFEST_PATH.is_file():
        raise ManifestError(
            f"Content catalog not found. Expected manifest at {MANIFEST_PATH}"
        )
    try:
        return Manifest.model_validate(
            json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        )
    except json.JSONDecodeError as e:
        raise ManifestError(f"Syntax error in manifest.json: {e}") from e
    except ValidationError as e:
        raise ManifestError(f"Invalid manifest data schema: {e}") from e
    except Exception as e:
        raise ManifestError(f"Unexpected error loading manifest: {e}") from e


def get_manifest_exercise(exercise_id: str) -> ManifestExercise:
    """
    Returns the ManifestExercise with the given ID
    Raises ExerciseNotFoundError if not found in the manifest
    """
    manifest = load_manifest()
    for exercise in manifest.exercises:
        if exercise.id == exercise_id:
            return exercise
    raise ExerciseNotFoundError(
        f"Exercise with ID '{exercise_id}' not found in manifest."
    )


def list_manifest_exercises() -> list[ManifestExercise]:
    """Returns all exercises defined in the manifest"""
    manifest = load_manifest()
    return manifest.exercises


def latest_content_version(manifest: Manifest) -> str:
    """Returns the version of the course content registry from the provided manifest."""
    return manifest.content_version
