"""
Validation pipeline orchestrator.

Coordinates the execution of the validation lifecycle for a given exercise file.
Ties together configuration, metadata, structural checks, type checks, and progress tracking.

Responsible for:
    - Resolving target exercises and loading their metadata.
    - Executing AST and Pyright validation phases in the correct order.
    - Short-circuiting execution (failing fast) if structural validation fails.
    - Localizing error messages based on user language configuration.
    - Recording user progress and attempt history.

Not responsible for:
    - Parsing AST trees or executing type-checking subprocesses directly.
    - Reading or writing raw JSON data to the filesystem.
"""

from pathlib import Path

from revex.core.models import (
    ExerciseMetadata,
    ExerciseNotFoundError,
    ValidationErrorRecord,
)
from revex.core.services.config import load_config
from revex.core.services.content import get_exercise_name, load_metadata
from revex.core.services.manifest import get_manifest_exercise, load_manifest
from revex.core.services.progress import record_attempt
from revex.core.validators.ast_validator import validate_ast
from revex.core.validators.pyright_validator import validate_pyright


def resolve_exercise_id(file_path: Path) -> str:
    """
    Infer the 4-digit exercise ID based on filesystem conventions.

    Attempts to extract the ID from the parent directory's naming convention
    (e.g., '0101-basic_type_hints'). If that fails, it checks the file's stem
    against known exercise names in the global manifest.

    Args:
        file_path: The absolute or relative path to the student's source file.

    Returns:
        The resolved 4-digit exercise ID as a string.

    Raises:
        ExerciseNotFoundError: If the ID cannot be inferred from the directory
            structure or matched within the manifest.
    """
    abs_path = file_path.resolve()
    # Check parent directory name (e.g. "0101-basic_type_hints")
    parent_name = abs_path.parent.name
    if len(parent_name) >= 4 and parent_name[:4].isdigit():
        return parent_name[:4]

    # Fallback: check the filename against exercise names in the manifest
    try:
        manifest = load_manifest()
        filename = abs_path.stem
        for ex in manifest.exercises:
            if get_exercise_name(ex) == filename:
                return ex.id
    except Exception:
        pass

    raise ExerciseNotFoundError(f"Could not resolve exercise ID for file: {file_path}")


def run_validation(file_path: Path) -> list[ValidationErrorRecord]:
    """
    Execute the full validation lifecycle for a given source file.

    Orchestrates the resolution of metadata, execution of structural (AST)
    and type (Pyright) checks, and records the completion status. Implements
    a fail-fast design: if AST validation fails, Pyright is skipped.

    Args:
        file_path: The filesystem path to the Python file to validate.

    Returns:
        A combined list of ValidationErrorRecord objects containing localized
        hints. Returns an empty list if all phases pass perfectly.
    """
    abs_path = file_path.resolve()

    # 1. Resolve exercise and metadata
    try:
        exercise_id = resolve_exercise_id(abs_path)
        exercise = get_manifest_exercise(exercise_id)
        metadata = load_metadata(exercise)
    except Exception as e:
        return [
            ValidationErrorRecord(
                error_code="RESOLUTION_ERROR",
                message=f"Error resolving exercise details: {e}",
            )
        ]

    # 2. Run AST validation
    errors = validate_ast(abs_path, metadata.validation)

    # 3. If AST errors exist, resolve translation hints and halt
    if errors:
        _resolve_hints(errors, metadata)
        record_attempt(exercise_id, completed=False)
        return errors

    # 4. Run Pyright validation
    pyright_errors = validate_pyright(abs_path)
    errors.extend(pyright_errors)

    # 5. Record attempt and completion
    completed = len(errors) == 0
    record_attempt(exercise_id, completed=completed)

    # 6. Resolve hints for any remaining errors (if applicable) and return
    _resolve_hints(errors, metadata)
    return errors


def _resolve_hints(
    errors: list[ValidationErrorRecord],
    metadata: ExerciseMetadata,
) -> None:
    """
    Map localized translation hints to a list of validation errors.

    Mutates the provided list of ValidationErrorRecord objects in-place,
    updating their message fields with domain-specific hints based on the
    user's configured language.

    Args:
        errors: The active list of validation errors to mutate.
        metadata: The exercise metadata containing the translation dictionaries.
    """
    try:
        config = load_config()
        if not config.settings.allow_hints:
            return
        lang = config.settings.language
    except Exception:
        lang = "en"

    # Fetch translation dictionary
    translation = metadata.translations.get(lang)
    if not translation:
        translation = metadata.translations.get("en")

    hints = {}
    if translation and translation.hints:
        hints = translation.hints.get("error_codes", {})

    for err in errors:
        if err.error_code in hints:
            err.message = hints[err.error_code]
