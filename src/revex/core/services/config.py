"""
User configuration management.

Responsible for:
    - loading user configuration
    - validating configuration values
    - updating configuration settings
    - persisting configuration changes

Not responsible for:
    - progress tracking
    - content discovery
    - exercise validation
"""
# usage: uv run revex set --parameter "value"

import tomllib
from pathlib import Path
from typing import cast

from revex.core.models import Config, ConfigError
from revex.core.services.paths import STATE_DIR

CONFIG_PATH: Path = STATE_DIR / "config.toml"


def load_config(default: bool = False) -> Config:
    """
    Reads the config.toml file using Python's built-in tomllib.
    Returns a validated Config Pydantic model. If the file doesn't exist,
    it returns a Config instance with default values.
    """
    if default:
        return Config()
    if not CONFIG_PATH.is_file():
        # Return the default configuration if the file does not exist
        return Config()
    with open(CONFIG_PATH, "rb") as file:
        try:
            return Config.model_validate(tomllib.load(file))
        except tomllib.TOMLDecodeError as e:
            raise ConfigError(f"Syntax error in configuration file: {e}") from e
        except Exception as e:
            raise ConfigError(f"Invalid configuration settings: {e}") from e


def save_config(config: Config) -> None:
    """
    Zero-dependency helper to serialize the Pydantic Config schema
    into standard TOML format and save it to the configuration file
    """
    # Ensure the target directory (.user_data) exists
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Dump the Pydantic model to a standard dictionary
    config_data = cast(
        dict[str, dict[str, bool | str | int | float]], config.model_dump()
    )

    toml_lines: list[str] = []

    for section_name, section_values in config_data.items():
        toml_lines.append(f"[{section_name}]")

        for key, value in section_values.items():
            if isinstance(value, bool):
                toml_lines.append(f"{key} = {'true' if value else 'false'}")
            elif isinstance(value, str):
                toml_lines.append(f'{key} = "{value}"')
            else:
                # Exhaustive type narrowing: Pyright knows this MUST be either int | float
                toml_lines.append(f"{key} = {value}")

        toml_lines.append("")

    # Write out the joined string
    _ = CONFIG_PATH.write_text("\n".join(toml_lines), encoding="utf-8")


if __name__ == "__main__":
    default_config: Config = load_config(default=True)
    print(default_config)
    save_config(default_config)
