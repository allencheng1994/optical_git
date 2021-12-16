import argparse
import json
import sys
import os
from pathlib import Path
from src import rep_manipulator
from src import config
from src import lens_test_case
from src.common import load_json_data, find_optical_repo_path
from src.extractor import log_data, export_figs


def go_extracting(args):
    if args.current:
        file_path = None
    else:
        repo = find_optical_repo_path()
        file_path = load_json_data(repo.joinpath(config.CONST["TRACKFILE"] + ".json"))[
            "file"
        ]
    log_data(file_path, args.refresh)


def go_exporting(args):
    if args.current:
        file_path = None
    else:
        repo = find_optical_repo_path()
        file_path = load_json_data(repo.joinpath(config.CONST["TRACKFILE"] + ".json"))[
            "file"
        ]
    export_figs(file_path)


def go_testing(args):
    lens_test_case.exc_projection_lens_test(args.show_skipped_list)


def type_formating(args):
    repo = find_optical_repo_path()
    if args.all:
        files = list(repo.glob(r"*.json"))
    else:
        files = [repo.joinpath(file + ".json") for file in args.file]
    for file in files:
        file_path = Path(os.path.abspath(file))
        with open(file_path, "r", encoding="utf-8") as infile:
            objs = (json.load(infile),)

        with open(file_path, "w", encoding="utf-8") as outfile:
            for obj in objs:
                json.dump(obj, outfile, indent=4)
                outfile.write("\n")


def repository_initialize(args):
    setting_templates = load_json_data(config.USR_CONFIG)
    rep_manipulator.repo_init(setting_templates["template"].get(args.template))


def repository_show(args):
    if args.item == "":
        rep_manipulator.repo_show_files()
    else:
        rep_manipulator.repo_show_items(args.item)


def repository_show_fig(args):
    if args.figure == "":
        rep_manipulator.repo_show_figs()
    else:
        rep_manipulator.repo_show_fig(args.figure)


def repository_diff_fig(args):
    try:
        rep_manipulator.repo_fig_diff(args.item, args.sha)
    except FileNotFoundError as e:
        print(e)


def repository_add(args):
    if len(args.added) >= 2:
        file, *added_items = args.added
        try:
            rep_manipulator.repo_add_item(file, added_items)
        except FileNotFoundError:
            print(
                "These items should be entered correctly and be in the correct order."
            )
    elif len(args.added) == 1:
        rep_manipulator.repo_add_file(*args.added)
    else:
        print("The number of arguments should be more than 1.")


def repository_rm(args):
    if len(args.removed) >= 2:
        file, *removed_items = args.removed
        try:
            rep_manipulator.repo_rm_item(file, removed_items)
        except FileNotFoundError:
            print(
                "These items should be entered correctly and be in the correct order."
            )
    elif len(args.removed) == 1:
        rep_manipulator.repo_rm_item(*args.removed)
    else:
        print("The number of arguments should be more than 1.")


def repository_modify(args):
    try:
        file, item, *val_str = args.modified
        rep_manipulator.repo_modify(file, item, val_str)
    except FileNotFoundError:
        print("The file is not found.")
    except KeyError:
        print("The item has not been added.")


def repository_collect(args):
    rep_manipulator.repo_collect()


def repository_pick_data(args):
    rep_manipulator.repo_pick_files(args.file, args.sha, suffix=".json")


def repository_pick_figs(args):
    rep_manipulator.repo_pick_files(args.file, args.sha, suffix=".png")


def change_tracking_file(args):
    rep_manipulator.repo_change_tracking_file(args.file)


def main():
    try:
        setting_templates = load_json_data(config.USR_CONFIG)
    except FileNotFoundError:
        setting_templates = config.LOGGER_TEMPLATE
        with open(config.USR_CONFIG, "w", encoding="utf-8") as f:
            data = setting_templates
            json.dump(data, f)

    template_choices = list(setting_templates["template"].keys())

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Initialize
    parser_init = subparsers.add_parser("init", help="Initiate the optical repository.")
    parser_init.add_argument(
        "-t", "--template", choices=template_choices, default=template_choices[0]
    )
    parser_init.set_defaults(func=repository_initialize)

    # Show the information
    parser_show = subparsers.add_parser(
        "show", help="Show the information in the repository."
    )
    parser_show.add_argument(
        "item",
        type=str,
        nargs="?",
        default="",
        help="The item which you want to get the information.",
    )
    parser_show.set_defaults(func=repository_show)

    # Show the figure
    parser_show_figs = subparsers.add_parser("show-fig", help="show the figure")
    parser_show_figs.add_argument(
        "figure",
        type=str,
        nargs="?",
        default="",
        help="The figure which you want to show.",
    )
    parser_show_figs.set_defaults(func=repository_show_fig)

    # Add items
    parser_add = subparsers.add_parser("add", help=f"Add the item to the file.")
    parser_add.add_argument(
        "added", type=str, nargs="+", help=f"The item you want to add."
    )
    parser_add.set_defaults(func=repository_add)

    # Remove items
    parser_rm = subparsers.add_parser("rm", help=f"Remove the item in the file.")
    parser_rm.add_argument(
        "removed", type=str, nargs="+", help=f"The item which you want to remove."
    )
    parser_rm.set_defaults(func=repository_rm)

    # Modify items
    parser_modify = subparsers.add_parser(
        "modify", aliases=["mod"], help="Modify the information in the item."
    )
    parser_modify.add_argument(
        "modified", type=str, nargs="+", help=f"The item which you want to modify."
    )
    parser_modify.set_defaults(func=repository_modify)

    # Extracting Data
    parser_extract = subparsers.add_parser(
        "extract", help="Extract the data from the simulation program."
    )
    parser_extract.add_argument(
        "--current",
        "-c",
        action="store_const",
        const=True,
        default=False,
        help="Extract the data from the current file.",
    )
    parser_extract.add_argument(
        "--refresh",
        "-r",
        action="store_const",
        const=True,
        default=False,
        help=(
            "When using this flag, the program will refresh the whole data in the data"
            " file."
        ),
    )
    parser_extract.set_defaults(func=go_extracting)

    # Exporting Figure
    parser_export_fig = subparsers.add_parser(
        "export", help="Export the figures from the simulation program."
    )
    parser_export_fig.add_argument(
        "--current",
        "-c",
        action="store_const",
        const=True,
        default=False,
        help="Export the figures from the current file.",
    )
    parser_export_fig.set_defaults(func=go_exporting)

    # Collecting Data
    parser_collect = subparsers.add_parser(
        "collect", help="Collect the data into a single file."
    )
    parser_collect.set_defaults(func=repository_collect)

    # Change default setting
    parser_default = subparsers.add_parser(
        "defaults",
        help="Use this function to change the default setting of optical git.",
    )

    # Track the optical design file
    parser_trackfile = subparsers.add_parser(
        "track", help="Change the tracking design."
    )
    parser_trackfile.add_argument("file", type=str)
    parser_trackfile.set_defaults(func=change_tracking_file)

    # Doing the test
    parser_testing = subparsers.add_parser("test", help="Executing the test.")
    parser_testing.add_argument(
        "--show-skipped-list",
        "-s",
        action="store_const",
        const=True,
        default=False,
        help=(
            "When using this flag, the program will list the tests you skipped in this"
            " term."
        ),
    )
    parser_testing.set_defaults(func=go_testing)

    # Format the json file
    parser_type_format = subparsers.add_parser(
        "format-type", aliases=["ft"], help="Formating the json file."
    )
    parser_type_format.add_argument(
        "file",
        nargs="*",
        type=str,
        help="The json file which you want to do formating.",
    )
    parser_type_format.add_argument(
        "--all", "-a", action="store_const", const=True, default=False
    )
    parser_type_format.set_defaults(func=type_formating)

    parser_pick_data = subparsers.add_parser(
        "pick-data",
        aliases=["pd"],
        help="copy the specific file from the specific version.",
    )

    parser_pick_data.add_argument("file", type=str, help="target")
    parser_pick_data.add_argument(
        "sha",
        nargs="+",
        type=str,
        help="The SHA or tag's value of the specific version. However, using tags is much better.",
    )
    parser_pick_data.set_defaults(func=repository_pick_data)

    parser_pick_figs = subparsers.add_parser(
        "pick-fig",
        aliases=["pf"],
        help="copy the specific figure from the specific version.",
    )

    parser_pick_figs.add_argument("figure", type=str, help="target")
    parser_pick_figs.add_argument(
        "sha",
        nargs="+",
        type=str,
        help="The SHA or tag's value of the specific version. However, using tags is much better.",
    )
    parser_pick_figs.set_defaults(func=repository_pick_figs)

    parser_diff_figs = subparsers.add_parser(
        "diff-fig",
        aliases=["df"],
        help="Compare the data figure between specifc version",
    )
    parser_diff_figs.add_argument("item", type=str, help="target")
    parser_diff_figs.add_argument(
        "sha",
        nargs="+",
        type=str,
        help="The SHA or tag's value of the specific version. However, using tags is much better.",
    )
    parser_diff_figs.set_defaults(func=repository_diff_fig)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
