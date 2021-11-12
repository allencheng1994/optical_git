import json
import sys
import re
import os
from functools import wraps
from pathlib import Path
from pathlib import PurePath
from optical_git.src import config


def has_optical_rep():
    current_path = Path.cwd()
    while current_path.parent != current_path:
        if current_path.joinpath(".optical_git").exists():
            return True
        current_path = current_path.parent
    if current_path.joinpath(".optical_git").exists():
        return True
    return False


def find_optical_rep_path():
    current_path = Path.cwd()
    while current_path.parent != current_path:
        if current_path.joinpath(".optical_git").exists():
            return current_path.joinpath(".optical_git")
        current_path = current_path.parent
    if current_path.joinpath(".optical_git").exists():
        return current_path.joinpath(".optical_git")
    sys.exit("Cannot find .optical_git")


def optical_init(template):
    if has_optical_rep():
        sys.exit("Repository already exists.")

    current_path = Path.cwd()
    rep_path = Path.cwd().joinpath(".optical_git")
    Path.mkdir(rep_path)
    for key_name in template:
        json_file = rep_path.joinpath(key_name + ".json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(template[key_name], f)


def optical_show_files():
    rep_path = find_optical_rep_path()
    json_files = list(rep_path.glob(r"*.json"))
    for file in json_files:
        name = re.sub(".json", "", file.name)
        print(name)


def optical_show_items(file_name):
    rep_path = find_optical_rep_path()
    file_name = file_name.lower()
    json_file = rep_path.joinpath(file_name + ".json")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for key in data:
        print(f'{key}: {data[key]}')


def optical_add_file(file):
    rep_path = find_optical_rep_path()
    file = file.lower()
    if file == config.LOG:
        exit_msg = f'The {config.LOG} should be created by using collect'
        sys.exit(exit_msg)
    json_file = rep_path.joinpath(file + ".json")
    if not json_file.exists():
        data = {}
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    else:
        print(f'{file} exists.')


def optical_add_item(file, item):
    rep_path = find_optical_rep_path()
    file = file.lower()
    if file in config.ONLY_PROGRAM:
        exit_msg = f'The value in {file} should not be changed by using added.'
        sys.exit(exit_msg)
    item = item.lower()
    json_file = rep_path.joinpath(file + ".json")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data.setdefault(item)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def optical_modify(file, item, val_str):
    rep_path = find_optical_rep_path()
    file = file.lower()
    if file in config.ONLY_PROGRAM:
        exit_msg = f'The value in {file} should not be changed by using modify.'
        sys.exit(exit_msg)
    item = item.lower()
    json_file = rep_path.joinpath(file + ".json")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if item not in data:
        raise KeyError
    data[item] = val_str
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def optical_rm_file(file):
    rep_path = find_optical_rep_path()
    file = file.lower()
    json_file = rep_path.joinpath(file + ".json")
    os.remove(json_file)


def optical_rm_item(file, item):
    rep_path = find_optical_rep_path()
    file = file.lower()
    item = item.lower()
    json_file = rep_path.joinpath(file + ".json")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data.pop(item)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def optical_collect():
    rep_path = find_optical_rep_path()
    log_file = rep_path.joinpath(config.LOG + ".json")
    json_files = list(rep_path.glob(r"*.json"))
    whole_data = {}
    for file in json_files:
        if file != log_file:
            name = re.sub(".json", "", file.name)
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                whole_data.setdefault(name, data)

    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(whole_data, f)


if __name__ == '__main__':
    pass
