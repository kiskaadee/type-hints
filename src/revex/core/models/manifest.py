"""
Manifest models.

Defines the structure of the content registry.
"""

from pydantic import BaseModel, Field

from revex.core.models.base import ExerciseBase


class ManifestExercise(ExerciseBase):
    """Schema representing an exercise record inside the manifest registry."""

    path: str


class Manifest(BaseModel):
    """Top-level manifest configuration mapping for manifest.json."""

    content_version: str
    exercises: list[ManifestExercise] = Field(default_factory=list[ManifestExercise])
