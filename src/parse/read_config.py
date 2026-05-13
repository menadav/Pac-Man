import json
from pathlib import Path
from typing import List
from src.parse.models import ParseConfig


def parse_config(path_av: str) -> ParseConfig:
    try:
        actual_path = Path(path_av)
        if actual_path.suffix != ".json":
            raise ValueError("[ERROR] Config file must be a .json")
        if not actual_path.exists():
            raise ValueError(f"[ERROR] {actual_path} not exist")
        if not actual_path.is_file():
            raise ValueError(f"[ERROR] {path_av} is a directory, not a file")
        line_valid: List[str] = []
        with open(actual_path, "r", encoding="utf-8") as f:
            for line in f:
                line_clean = line.strip()
                if not line_clean or line_clean.startswith("#"):
                        continue
                line_valid.append(line_clean)
        string_json = "".join(line_valid)
        dict_json = json.loads(string_json)
        return ParseConfig(**dict_json)
    except json.JSONDecodeError:
        raise ValueError("[ERROR] Invalid JSON format")
    except FileNotFoundError:
         raise ValueError("[ERROR] File not found")
    except PermissionError:
         raise ValueError("[ERROR] Permission errors")
         