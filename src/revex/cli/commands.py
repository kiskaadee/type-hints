"""
CLI Commands Handlers.

Bridges the presentation layer with the core domain services.
Formats output and handles terminal stdout/stderr logic.
"""


from revex.core.models import ConfigError
from revex.core.services.config import load_config, save_config
from revex.core.services.setup import initialize_environment
from revex.core.services.sync import sync_workspace


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
    print(f"Validating solution: {target or 'current directory'}...")


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
    print(f"Rendering description for: {target}...")
