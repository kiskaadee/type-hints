"""
Configuration models.

Defines the structure of user configuration
data used throughout the application.
"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    """User personal details."""

    nickname: str


class Settings(BaseModel):
    """User-specific settings configuration."""

    language: Literal["en", "es"] = Field(default="en")
    allow_hints: bool = Field(
        default=True,
        description="Output static hints when validator finds an error.",
    )
    allow_llm: bool = Field(
        default=False,
        description="Output LLM-powered personalized hints when validator finds an error",
    )
    allow_glow: bool = Field(
        default=False,
        description="Terminal outputs decorated with glow (requires glow dependency)",
    )

    @field_validator("allow_llm")
    @classmethod
    def validate_allow_llm(cls, value: bool) -> bool:
        """Ensures allow_llm remains False until the feature is implemented."""
        if value is True:
            raise ValueError(
                "LLM-powered interactive hints are not yet supported. Coming soon!"
            )
        return value

    # @field_validator("language")
    # @classmethod
    # def validate_language(cls, value: str) -> str:
    #     # check lenght
    #     if not len(value) == 2:
    #         raise ValueError("Language code must be exactly two letters long.")

    #     # supported languages
    #     allowed_languages = ["en", "es"]
    #     if value not in allowed_languages:
    #         raise ValueError("Language configuration not supported")


class Config(BaseModel):
    """Top-level configuration schema for config.toml."""

    # 1. Python reads this class definition
    # 2. It registers `Settings` as a factory function, but does NOT call
    settings: Settings = Field(default_factory=Settings)


# Example of loading from a TOML file
# from models import Config
# def load_config(file_path: str) -> Config:
#     with open(file_path, "rb") as f:
#         toml_data = tomllib.load(f)

#     # Unpack the parsed TOML dictionary into the Config model
#     return Config(**toml_data)
