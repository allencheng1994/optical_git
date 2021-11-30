import json
import sys
import re
import os
from git import Repo
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
from . import config
from .common import exist_optical_repo
from .common import find_optical_repo_path
from .common import is_number
from .config import CONST


def repo_init(template):
    if exist_optical_repo():
        sys.exit("Repository already exists.")

    Repo.init(Path.cwd())
    repo_path = Path.cwd().joinpath(".optical_git")
    Path.mkdir(repo_path)
    for key_name in template:
        json_file = repo_path.joinpath(key_name + ".json")
        with open(json_file, "w", encoding="utf-8") as jfile:
            json.dump(template[key_name], jfile)


def repo_show_files():
    repo_path = find_optical_repo_path()
    json_files = list(repo_path.glob(r"*.json"))
    for file in json_files:
        name = re.sub(".json", "", file.name)
        print(name)


def repo_show_items(file_name):
    repo_path = find_optical_repo_path()
    file_name = file_name.lower()
    json_file = repo_path.joinpath(file_name + ".json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    for key in data:
        print(f"{key}: {data[key]}")


def repo_show_figs():
    repo_path = find_optical_repo_path()
    figs = list(repo_path.glob(r"*.wmf"))
    for fig in figs:
        name = re.sub(".wmf", "", fig.name)
        print(name)


def repo_show_fig(fig_name):
    pass


def repo_add_file(file):
    repo_path = find_optical_repo_path()
    file = file.lower()
    if file == config.LOG:
        exit_msg = f'The {config.LOG} should be created by using "collect"'
        sys.exit(exit_msg)
    json_file = repo_path.joinpath(file + ".json")
    if not json_file.exists():
        data = {}
        with open(json_file, "w", encoding="utf-8") as jfile:
            json.dump(data, jfile)
    else:
        print(f"{file} exists.")


def repo_add_item(file, items):
    repo_path = find_optical_repo_path()
    file = file.lower()
    adds = [item.lower() for item in items]
    json_file = repo_path.joinpath(file + ".json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    for add_item in adds:
        data.setdefault(add_item)
    with open(json_file, "w", encoding="utf-8") as jfile:
        json.dump(data, jfile)


def repo_modify(file, item, val_str):
    repo_path = find_optical_repo_path()
    file = file.lower()
    if file in config.ONLY_PROGRAM:
        exit_msg = f"The value in {file} should not be changed by using modify."
        sys.exit(exit_msg)
    if item == "file":
        exit_msg = (
            f"If you want to change the tracking file, you should use 'file' to"
            f" modify it."
        )
        sys.exit(exit_msg)
    item = item.lower()
    json_file = repo_path.joinpath(file + ".json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    if item not in data:
        raise KeyError(f"{item} is not in data.")

    if len(val_str) > 1:
        val_list = []
        for val in val_str:
            val_converted = float(val) if is_number(val) else val
            val_list.append(val_converted)
        data[item] = val_list
    else:
        val, *_ = val_str
        data[item] = float(val) if is_number(val) else val

    with open(json_file, "w", encoding="utf-8") as jfile:
        json.dump(data, jfile)


def repo_rm_file(file):
    repo_path = find_optical_repo_path()
    file = file.lower()
    json_file = repo_path.joinpath(file + ".json")
    os.remove(json_file)


def repo_rm_item(file, items):
    repo_path = find_optical_repo_path()
    file = file.lower()
    remove_items = [item.lower() for item in items]
    json_file = repo_path.joinpath(file + ".json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    for item in remove_items:
        data.pop(item)
    with open(json_file, "w", encoding="utf-8") as jfile:
        json.dump(data, jfile)


def repo_collect():
    repo_path = find_optical_repo_path()
    log_file = repo_path.joinpath(CONST["LOG"] + ".json")
    criterion_file = repo_path.joinpath(CONST["CRITERION"] + ".json")
    json_files = list(repo_path.glob(r"*.json"))
    whole_data = {}
    for file in json_files:
        if file != log_file or file != criterion_file:
            name = re.sub(".json", "", file.name)
            with open(file, "r", encoding="utf-8") as jfile:
                data = json.load(jfile)
                whole_data.setdefault(name, data)

            with open(file, "w", encoding="utf-8") as outfile:
                json.dump(data, outfile, indent=4)
                outfile.write("\n")

    with open(log_file, "w", encoding="utf-8") as jfile:
        json.dump(whole_data, jfile, indent=4)


def repo_change_tracking_file(file):
    repo_path = find_optical_repo_path()
    folder = repo_path.parent
    file_path = Path(os.path.abspath(file))
    if folder not in file_path.parents:
        sys.exit(
            """
            You should initialize the repository first.
            Your repository parent folder should be the
            parent of the lens file.
            """
        )

    json_file = repo_path.joinpath("file.json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    data["file"] = str(file_path.absolute())
    with open(json_file, "w", encoding="utf-8") as jfile:
        json.dump(data, jfile)


if __name__ == "__main__":
    pass
