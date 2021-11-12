import argparse
import json
import sys
from optical_git.src import info
from optical_git.src import config


def load_custom_templates(json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        data = json.load(f)

    return data


def system_initialize(args):
    templates = load_custom_templates(config.USR_CONFIG)
    info.optical_init(templates[args.template])


def system_show(args):
    if args.item == '':
        info.optical_show_files()
    else:
        info.optical_show_items(args.item)


def system_add(args):
    if len(args.added) == 2:
        try:
            info.optical_add_item(*args.added)
        except FileNotFoundError:
            print(
                "These items should be entered correctly and be in the correct order."
            )
    elif len(args.added) == 1:
        info.optical_add_file(*args.added)
    else:
        print("The number of arguments should be 1 or 2.")


def system_rm(args):
    if len(args.removed) == 2:
        try:
            info.optical_rm_item(*args.removed)
        except FileNotFoundError:
            print(
                "These items should be entered correctly and be in the correct order."
            )
    elif len(args.removed) == 1:
        info.optical_rm_file(*args.removed)
    else:
        print("The number of arguments should be 1 or 2.")


def system_modify(args):
    try:
        info.optical_modify(*args.modified)
    except FileNotFoundError:
        print("The file is not found.")
    except KeyError:
        print("The item has not been added.")


def system_collect(args):
    info.optical_collect()


def main():
    try:
        setting_templates = load_custom_templates(config.USR_CONFIG)
    except:
        setting_templates = config.PROJECTION_LENS_BASIC_TEMPLATE
        with open(config.USR_CONFIG, 'w', encoding='utf-8') as f:
            data = {"PROJECTION_LENS": config.PROJECTION_LENS_BASIC_TEMPLATE}
            json.dump(data, f)

    template_choices = list(setting_templates.keys())

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_init = subparsers.add_parser("init")
    parser_show = subparsers.add_parser("show")
    parser_add = subparsers.add_parser("add")
    parser_rm = subparsers.add_parser("rm")
    parser_modify = subparsers.add_parser("modify")
    parser_collect = subparsers.add_parser("collect")

    parser_init.add_argument(
        '-t', '--template', choices=template_choices, default=template_choices[0]
    )
    parser_init.set_defaults(func=system_initialize)

    parser_show.add_argument("item", type=str, nargs="?", default='')
    parser_show.set_defaults(func=system_show)

    parser_add.add_argument("added", type=str, nargs='+')
    parser_add.set_defaults(func=system_add)

    parser_rm.add_argument("removed", type=str, nargs='+')
    parser_rm.set_defaults(func=system_rm)

    parser_modify.add_argument("modified", type=str, nargs=3)
    parser_modify.set_defaults(func=system_modify)

    parser_collect.set_defaults(func=system_collect)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
