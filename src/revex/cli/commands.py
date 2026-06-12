"""
CLI Commands Handlers.

Bridges the presentation layer with the core domain services.
Formats output and handles terminal stdout/stderr logic.
"""


from pathlib import Path
import subprocess

from revex.core.models import ConfigError, ExerciseNotFoundError
from revex.core.services.config import load_config, save_config
from revex.core.services.content import load_problem_description
from revex.core.services.glow_helper import get_glow_install_advice, is_glow_available
from revex.core.services.manifest import get_manifest_exercise, load_manifest
from revex.core.services.progress import load_progress
from revex.core.services.setup import initialize_environment
from revex.core.services.sync import sync_workspace
from revex.core.validators import run_validation


def execute_setup() -> None:
    """Handles 'revex setup' command logic."""
    print("Setting up local workspace...")
    try:
        initialize_environment()
        print("Environment successfully initialized!")
    except Exception as e:
        print(f"Error during initialization: {e}")


def execute_status() -> None:
    """Handles 'revex status' command logic."""
    print("Displaying current progress...")


def execute_sync() -> None:
    """Handles 'revex sync' command logic."""
    print("Synchronizing workspace exercises...")
    try:
        summary = sync_workspace()
    except Exception as e:
        print(f"Error executing workspace synchronization: {e}")
        return

    for record in summary.records:
        if record.status == "added":
            print(f"  [+] Added:   [{record.exercise_id}] {record.exercise_name}")
        elif record.status == "failed":
            print(f"  [x] Failed:  [{record.exercise_id}] {record.exercise_name} ({record.reason})")

    print("\nSynchronization complete:")
    print(f"  Added:   {summary.added_count}")
    print(f"  Skipped: {summary.skipped_count}")
    print(f"  Failed:  {summary.failed_count}")


def execute_check(target: str | None) -> None:
    """Handles 'revex check' command logic."""
    if target:
        target_path = Path(target)
    else:
        cwd = Path.cwd()
        py_files = list(cwd.glob("*.py"))
        filtered_files = [f for f in py_files if not f.name.startswith("__") and f.name != "conftest.py"]
        if not filtered_files:
            print("Error: No Python solution file (*.py) found in the current directory.")
            print("Usage: revex check <file_path>")
            return
        target_path = filtered_files[0]

    if not target_path.is_file():
        print(f"Error: Target path '{target_path}' is not a valid file.")
        return

    print(f"Validating solution: {target_path.name}...")
    try:
        errors = run_validation(target_path)
    except Exception as e:
        print(f"Error during validation: {e}")
        return

    if not errors:
        print(f"\n✓ {target_path.name}: All checks passed! Lesson completed.")
    else:
        print(f"\n✗ {target_path.name}: Validation failed with {len(errors)} error(s):")
        for err in errors:
            line_str = f"Line {err.line_number}: " if err.line_number else ""
            print(f"  - {line_str}{err.message} [{err.error_code}]")


def execute_set(language: str | None) -> None:
    """Handles 'revex set' command logic."""
    try:
        config = load_config()
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return

    if language:
        if language in ("en", "es"):
            try:
                config.settings.language = language
                save_config(config)
                print(f"Language successfully set to: {language}")
            except Exception as e:
                print(f"Error updating configuration: {e}")
        else:
            print(f"Unsupported language: {language}")
    else:
        print("Current Configuration:")
        print(f"  Language: {config.settings.language}")
        print(f"  Allow Hints: {config.settings.allow_hints}")
        print(f"  Allow LLM: {config.settings.allow_llm}")
        print(f"  Allow Glow: {config.settings.allow_glow}")



def execute_view(target: str) -> None:
    """Handles 'revex view' command logic."""
    try:
        config = load_config()
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return

    # 1. Resolve exercise
    exercise = None
    if target == "next":
        try:
            progress = load_progress()
            manifest = load_manifest()
            for ex in manifest.exercises:
                completed = False
                if ex.id in progress.completed_exercises:
                    completed = progress.completed_exercises[ex.id].completed
                if not completed:
                    exercise = ex
                    break
            if not exercise:
                print("Congratulations! All exercises are completed!")
                return
        except Exception as e:
            print(f"Error checking progress: {e}")
            return
    else:
        try:
            exercise = get_manifest_exercise(target)
        except ExerciseNotFoundError:
            print(f"Error: Exercise '{target}' not found in the content registry.")
            return
        except Exception as e:
            print(f"Error loading manifest: {e}")
            return

    # 2. Load problem description
    try:
        markdown_content = load_problem_description(exercise, lang=config.settings.language)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Error loading problem description: {e}")
        return

    # 3. Render problem description
    if config.settings.allow_glow:
        if is_glow_available():
            try:
                subprocess.run(["glow", "-"], input=markdown_content, text=True, check=True)
                return
            except Exception as e:
                print(f"Error rendering with glow: {e}")
                print("Falling back to raw text output...\n")
        else:
            print("Warning: 'allow_glow' is enabled, but the 'glow' binary was not found in your PATH.")
            print(get_glow_install_advice())
            print("\nFalling back to raw text output...\n")

    # Fallback raw markdown display
    print(markdown_content)
