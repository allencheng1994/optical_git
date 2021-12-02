import json
import sys
from pathlib import Path
from .config import CONST


def load_json_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def is_number(val_str):
    try:
        float(val_str)
        return True
    except ValueError:
        return False


def exist_optical_repo():
    current_path = Path.cwd()
    while current_path.parent != current_path:
        if current_path.joinpath(CONST["OPTICAL-GIT"]).exists():
            return True
        current_path = current_path.parent
    if current_path.joinpath(CONST["OPTICAL-GIT"]).exists():
        return True
    return False


def find_optical_repo_path():
    current_path = Path.cwd()
    while current_path.parent != current_path:
        if current_path.joinpath(CONST["OPTICAL-GIT"]).exists():
            return current_path.joinpath(CONST["OPTICAL-GIT"])
        current_path = current_path.parent
    if current_path.joinpath(CONST["OPTICAL-GIT"]).exists():
        return current_path.joinpath(CONST["OPTICAL-GIT"])
    # raise FileNotFoundError
    sys.exit(f"Cannot find {CONST["OPTICAL-GIT"]}")


if __name__ == "__main__":
    pass
