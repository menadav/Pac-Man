"""Pydantic models for game configuration and highscores."""

try:
    from pydantic import BaseModel, Field, field_validator
except ImportError:
    raise ValueError("[ERROR] Install Pydantic")

from typing import Any, List

LEVEL_MIN_SIZE: int = 8
LEVEL_MAX_SIZE: int = 40


class LevelConfig(BaseModel):
    """Configuration schema for an individual game level."""
    level_id: int = 1
    width: int = 20
    height: int = 20
    pacgum: int = 42
    level_max_time: int = 90

    @field_validator("width", "height")
    @classmethod
    def clamp_dimension(cls, v: int, info: Any) -> int:
        """Validate and clamp maze dimensions within safe execution ranges."""
        if not isinstance(v, int) or v < LEVEL_MIN_SIZE:
            print(
                f"[CONFIG WARNING] {info.field_name}={v} is too small "
                f"(min {LEVEL_MIN_SIZE}). Clamped to {LEVEL_MIN_SIZE}."
            )
            return LEVEL_MIN_SIZE
        if v > LEVEL_MAX_SIZE:
            print(
                f"[CONFIG WARNING] {info.field_name}={v} is too large "
                f"(max {LEVEL_MAX_SIZE}, the maze generator is recursive). "
                f"Clamped to {LEVEL_MAX_SIZE}."
            )
            return LEVEL_MAX_SIZE
        return v

    @field_validator("pacgum")
    @classmethod
    def clamp_pacgum(cls, v: int, info: Any) -> int:
        """Ensure the pacgum count is non-negative."""
        if v < 0:
            print(f"[CONFIG WARNING] pacgum={v} is invalid. Using 0 (fill the maze).")
            return 0
        return v

    @field_validator("level_max_time")
    @classmethod
    def clamp_time(cls, v: int, info: Any) -> int:
        """Guarantee a valid level time limit or fallback to default."""
        if v < 20:
            security_default = int(cls.model_fields[info.field_name].default)
            print(
                f"[CONFIG WARNING] {info.field_name}. Using default: {security_default}"
            )
            return security_default
        if v > 99999999999:
            security_default = int(cls.model_fields[info.field_name].default)
            print(
                f"[CONFIG WARNING] {info.field_name}. Using default: {security_default}"
            )
            return 99999999999
        return v


class ParseConfig(BaseModel):
    """Global configuration schema for the Pac-Man game."""
    file: str = Field(default="highscores.json", alias="highscore_filename")
    seed: int = 42
    lives: int = 3
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    levels: List[LevelConfig]

    @field_validator("lives")
    @classmethod
    def clamp_lives(cls, v: int, info: Any) -> int:
        """Validate that the player starts with at least 1 life."""
        if v < 1:
            print(f"[CONFIG WARNING] lives={v} is invalid. Using default: 3")
            return 3
        if v > 9:
            print(f"[CONFIG WARNING] lives={v} is too high. Using default: 9")
            return 9
        return v

    @field_validator("levels")
    @classmethod
    def check_unique(cls, v: List[LevelConfig]) -> List[LevelConfig]:
        """Ensure each level has a unique ID, resolving duplicates dynamically."""
        ids_regist: set[int] = set()
        for level in v:
            if level.level_id in ids_regist:
                new_id = max(ids_regist) + 1 if ids_regist else 1
                print(
                    f"[CONFIG WARNING] ID {level.level_id} is repeated."
                    f" Fixed to: {new_id}"
                )
                level.level_id = new_id
            ids_regist.add(level.level_id)
        return v

    @field_validator(
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "seed",
    )
    @classmethod
    def clamp_points(cls, v: int, info: Any) -> int:
        """Prevent negative scoring or seeding values across configuration parameters."""
        if v < 0:
            security_default = int(cls.model_fields[info.field_name].default)
            print(
                f"[CONFIG WARNING] {info.field_name} cannot be negative "
                f"({v}). Using default: {security_default}"
            )
            return security_default
        if v > 300:
            security_default = int(cls.model_fields[info.field_name].default)
            print(
                f"[CONFIG WARNING] {info.field_name} cannot be negative "
                f"({v}). Using default: {security_default}"
            )
            return security_default
        return v


class HighScoreEntry(BaseModel):
    """Data structure for an individual highscore record."""

    name: str
    score: int

    @field_validator("name")
    @classmethod
    def check_name(cls, v: str) -> str:
        """Validate player name format: alphanumeric, spaces, and max 10 characters."""
        v = v.strip()
        if not v:
            raise ValueError("name must not be empty")
        if len(v) > 10:
            v = v[:10]
        if not all(c.isalnum() or c == " " for c in v):
            raise ValueError("name must contain only letters, digits and spaces")
        return v

    @field_validator("score")
    @classmethod
    def check_score(cls, v: int) -> int:
        """Verify that the highscore is a non-negative integer."""
        if v < 0:
            raise ValueError("score must be a non-negative integer")
        return v
