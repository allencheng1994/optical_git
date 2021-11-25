import json
import sys
from pathlib import Path


def load_json_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def exist_optical_repo():
    current_path = Path.cwd()
    while current_path.parent != current_path:
        if current_path.joinpath(".optical_git").exists():
            return True
        current_path = current_path.parent
    if current_path.joinpath(".optical_git").exists():
        return True
    return False


def find_optical_repo_path():
    current_path = Path.cwd()
    while current_path.parent != current_path:
        if current_path.joinpath(".optical_git").exists():
            return current_path.joinpath(".optical_git")
        current_path = current_path.parent
    if current_path.joinpath(".optical_git").exists():
        return current_path.joinpath(".optical_git")
    raise FileNotFoundError
    # sys.exit("Cannot find .optical_git")


if __name__ == "__main__":
    pass
