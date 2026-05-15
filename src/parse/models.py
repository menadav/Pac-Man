try:
    from pydantic import BaseModel, Field, field_validator
except ImportError:
    raise ValueError("[ERROR] Install Pydantic")
from typing import List

class LevelConfig(BaseModel):
    level_id: int
    width: int = 20
    height: int = 20
    pacgum: int = 42
    level_max_time: int = 90

    @field_validator('width', 'height', 'pacgum', 'level_max_time')
    @classmethod
    def clamp_default(cls, v: int, info):
        if v < 1:
            security_default = cls.model_fields[info.field_name].default
            print(
                    f"[CONFIG WARNING] {info.field_name}. Using default"
                    f": {security_default}"
                    )
            return security_default
        return v


class ParseConfig(BaseModel):
    file: str = Field(default="highscores.json", alias="highscore_filename")
    seed: int = 42
    lives: int = 3
    points_per_pacgum: int = 10 
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    levels: List[LevelConfig]

    @field_validator('levels')
    @classmethod
    def check_unique(cls, v: List[LevelConfig]):
        ids_regist = set()
        for levels in v:
            if levels.level_id in ids_regist:
                new_id = max(ids_regist) + 1 if ids_regist else 1
                print(
                    f"[CONFIG WARNING] ID {levels.level_id} is repeated."
                    f" Fixed to: {new_id}"
                    )
            ids_regist.add(levels.level_id)
        return v
    @field_validator(
        'points_per_pacgum',
        'points_per_super_pacgum',
        'points_per_ghost',
        'seed'
    )
    @classmethod
    def clamp_points(cls, v: int, info):
        if v < 0:
            security_default = cls.model_fields[info.field_name].default
            print(f"[CONFIG WARNING] {info.field_name} cannot be negative ({v}). "
                  f"Using default: {security_default}")
            return security_default
        return v

class HighScoreEntry(BaseModel):
    name: str
    score: int
