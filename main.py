import argparse
import json
import sys
from src import rep_manipulator
from src import config
from src.common import load_json_data
from src.extractor import log_data


def go_extracting(args):
    pass


def repository_initialize(args):
    templates = load_json_data(config.USR_CONFIG)['template']
    rep_manipulator.repo_init(templates[args.template])


def repository_show(args):
    if args.item == '':
        rep_manipulator.repo_show_files()
    else:
        rep_manipulator.repo_show_items(args.item)


def repository_add(args):
    if len(args.added) == 2:
        try:
            rep_manipulator.repo_add_item(*args.added)
        except FileNotFoundError:
            print(
                f"These items should be entered correctly and be in the correct order."
            )
    elif len(args.added) == 1:
        rep_manipulator.repo_add_file(*args.added)
    else:
        print(f"The number of arguments should be 1 or 2.")


def repository_rm(args):
    if len(args.removed) == 2:
        try:
            rep_manipulator.repo_rm_item(*args.removed)
        except FileNotFoundError:
            print(
                f"These items should be entered correctly and be in the correct order."
            )
    elif len(args.removed) == 1:
        rep_manipulator.repo_rm_item(*args.removed)
    else:
        print(f"The number of arguments should be 1 or 2.")


def repository_modify(args):
    try:
        rep_manipulator.repo_modify(*args.modified)
    except FileNotFoundError:
        print(f"The file is not found.")
    except KeyError:
        print(f"The item has not been added.")


def repository_collect(args):
    rep_manipulator.repo_collect()


def change_tracking_file(args):
    rep_manipulator.repo_change_tracking_file(args.file)


def main():
    try:
        setting_templates = load_json_data(config.USR_CONFIG)
    except FileNotFoundError:
        setting_templates = config.LOGGER_TEMPLATE
        with open(config.USR_CONFIG, 'w', encoding='utf-8') as f:
            data = setting_templates
            json.dump(data, f)

    template_choices = list(setting_templates['template'].keys())

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_init = subparsers.add_parser("init")
    parser_show = subparsers.add_parser("show")
    parser_add = subparsers.add_parser("add")
    parser_rm = subparsers.add_parser("rm")
    parser_modify = subparsers.add_parser("modify")
    parser_extract = subparsers.add_parser("extract")
    parser_collect = subparsers.add_parser("collect")
    parser_default = subparsers.add_parser("defaults")
    parser_trackfile = subparsers.add_parser("trackfile")

    parser_init.add_argument(
        '-t', '--template', choices=template_choices, default=template_choices[0]
    )
    parser_init.set_defaults(func=repository_initialize)

    parser_show.add_argument("item", type=str, nargs="?", default='')
    parser_show.set_defaults(func=repository_show)

    parser_add.add_argument("added", type=str, nargs='+')
    parser_add.set_defaults(func=repository_add)

    parser_rm.add_argument("removed", type=str, nargs='+')
    parser_rm.set_defaults(func=repository_rm)

    parser_modify.add_argument("modified", type=str, nargs=3)
    parser_modify.set_defaults(func=repository_modify)

    parser_collect.set_defaults(func=repository_collect)

    parser_trackfile.add_argument("file", type=str)
    parser_trackfile.set_defaults(func=change_tracking_file)

    parser_extract.set_defaults(func=go_extracting)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
