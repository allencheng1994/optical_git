import json
import sys
import re
import win32com.client
import pyzdde.zdde as pyz
from win32com.client import Dispatch
from pathlib import Path
from wand.image import Image
from .config import CONST


class CodeVStandaloneApplication(object):
    def __init__(self):
        self.TheApplication = win32com.client.Dispatch("CodeV.Command.102")
        self.TheApplication.SetStartingDirectory("C:/CVUSER")
        self.TheApplication.StartCodev()

    def __del__(self):
        if self.TheApplication is not None:
            self.TheApplication.StopCodev()
            self.TheApplication = None


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


class ZmxFileParser:
    def __init__(self, file):
        self.__file = file
        self.stop = self.__get_stop_zmx()
        self.material = self.__get_material_zmx()
        self.mid = self.__gen_mid()

    def __get_stop_zmx(self):
        with open(self.__file, "r") as f:
            data = f.read()
            pattern = re.compile(r"SURF (\d+)\n  STOP")
            match = pattern.search(data)
            return int(match.group(1))

    def __get_material_zmx(self):
        with open(self.__file, "r") as f:
            data = f.read()
            pattern = re.compile("GLAS.{,40}0")
            match = pattern.findall(data)
            material = []
            for string in match:
                material.append(string.split()[1])
        return material

    def __gen_mid(self):
        mid = 0
        if self.stop != 1:
            mid = int(self.stop / 2 - 1)
        return mid


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
