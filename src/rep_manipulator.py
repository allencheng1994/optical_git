import json
import sys
import re
import os
from pathlib import Path
from . import config
from .common import exist_optical_repo
from .common import find_optical_repo_path


def repo_init(template):
    if exist_optical_repo():
        sys.exit("Repository already exists.")

    current_path = Path.cwd()
    rep_path = Path.cwd().joinpath(".optical_git")
    Path.mkdir(rep_path)
    for key_name in template:
        json_file = rep_path.joinpath(key_name + ".json")
        with open(json_file, "w", encoding="utf-8") as jfile:
            json.dump(template[key_name], jfile)


def repo_show_files():
    rep_path = find_optical_repo_path()
    json_files = list(rep_path.glob(r"*.json"))
    for file in json_files:
        name = re.sub(".json", "", file.name)
        print(name)


def repo_show_items(file_name):
    rep_path = find_optical_repo_path()
    file_name = file_name.lower()
    json_file = rep_path.joinpath(file_name + ".json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    for key in data:
        print(f"{key}: {data[key]}")


def repo_add_file(file):
    rep_path = find_optical_repo_path()
    file = file.lower()
    if file == config.LOG:
        exit_msg = f'The {config.LOG} should be created by using "collect"'
        sys.exit(exit_msg)
    json_file = rep_path.joinpath(file + ".json")
    if not json_file.exists():
        data = {}
        with open(json_file, "w", encoding="utf-8") as jfile:
            json.dump(data, jfile)
    else:
        print(f"{file} exists.")


def repo_add_item(file, item):
    rep_path = find_optical_repo_path()
    file = file.lower()
    item = item.lower()
    json_file = rep_path.joinpath(file + ".json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    data.setdefault(item)
    with open(json_file, "w", encoding="utf-8") as jfile:
        json.dump(data, jfile)


def repo_modify(file, item, val_str):
    rep_path = find_optical_repo_path()
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
    json_file = rep_path.joinpath(file + ".json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    if item not in data:
        raise KeyError(f"{item} is not in data.")
    data[item] = val_str
    with open(json_file, "w", encoding="utf-8") as jfile:
        json.dump(data, jfile)


def repo_rm_file(file):
    rep_path = find_optical_repo_path()
    file = file.lower()
    json_file = rep_path.joinpath(file + ".json")
    os.remove(json_file)


def repo_rm_item(file, item):
    rep_path = find_optical_repo_path()
    file = file.lower()
    item = item.lower()
    json_file = rep_path.joinpath(file + ".json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    data.pop(item)
    with open(json_file, "w", encoding="utf-8") as jfile:
        json.dump(data, jfile)


def repo_collect():
    rep_path = find_optical_repo_path()
    log_file = rep_path.joinpath(config.LOG + ".json")
    json_files = list(rep_path.glob(r"*.json"))
    whole_data = {}
    for file in json_files:
        if file != log_file:
            name = re.sub(".json", "", file.name)
            with open(file, "r", encoding="utf-8") as jfile:
                data = json.load(jfile)
                whole_data.setdefault(name, data)

    with open(log_file, "w", encoding="utf-8") as jfile:
        json.dump(whole_data, jfile)


def repo_change_tracking_file(file):
    rep_path = find_optical_repo_path()
    folder = rep_path.parent
    file_path = Path(os.path.abspath(file))
    if folder not in file_path.parents:
        sys.exit(
            """
            You should initialize the repository first. 
            Your repository parent folder should be the 
            parent of the lens file.
            """
        )

    json_file = rep_path.joinpath("file.json")
    with open(json_file, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
    data["file"] = str(file_path.absolute())
    with open(json_file, "w", encoding="utf-8") as jfile:
        json.dump(data, jfile)


if __name__ == "__main__":
    pass
