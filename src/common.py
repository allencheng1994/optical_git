import json
import sys
import re
import pyzdde.zdde as pyz
from pathlib import Path
from wand.image import Image
from .config import CONST


class Zemax14(object):
    """docstring for Zemax14"""

    def __init__(self, file):
        self._file = file

    def __enter__(self):
        self._channel = pyz.createLink()
        if self._file:
            self._channel.zLoadFile(self._file)
        return self._channel

    def __exit__(self, exc_type, exc_val, exc_tb):
        pyz.closeLink()


def convert_wmf(img: Path, filetype: str = "png") -> None:
    filepath = img.resolve()
    parent = filepath.parent
    newfilename = re.sub(".wmf", "", filepath.name)
    newfilepath = parent.joinpath(newfilename + "." + filetype).resolve()
    with Image(filename=filepath) as image_file:
        image_file.format = filetype
        image_file.save(filename=newfilepath)
    img.unlink(missing_ok=True)


def load_json_data(json_file: Path) -> dict:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def is_number(val_str: str) -> bool:
    try:
        float(val_str)
        return True
    except ValueError:
        return False


def exist_optical_repo() -> bool:
    current_path = Path.cwd()
    while current_path.parent != current_path:
        if current_path.joinpath(CONST["OPTICAL-GIT"]).exists():
            return True
        current_path = current_path.parent
    if current_path.joinpath(CONST["OPTICAL-GIT"]).exists():
        return True
    return False


def find_optical_repo_path() -> Path:
    current_path = Path.cwd()
    while current_path.parent != current_path:
        if current_path.joinpath(CONST["OPTICAL-GIT"]).exists():
            return current_path.joinpath(CONST["OPTICAL-GIT"])
        current_path = current_path.parent
    if current_path.joinpath(CONST["OPTICAL-GIT"]).exists():
        return current_path.joinpath(CONST["OPTICAL-GIT"])
    raise FileNotFoundError("Cannot find .optical-git")
    # sys.exit(f"Cannot find {CONST["OPTICAL-GIT"]}")


if __name__ == "__main__":
    pass
