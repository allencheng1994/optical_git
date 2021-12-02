from pathlib import Path
from pathlib import PurePath

# Installed file
INSTALLED_FOLDER = PurePath("D:/Code/Python_Code/optical_git")
USR_CONFIG = INSTALLED_FOLDER.joinpath("usr_config.json")
CONFIG_FOLDER = INSTALLED_FOLDER.joinpath("config/")

# The constant variable in system
CONST = {
    "OPTICAL-GIT": ".optical-git",
    "TRACKFILE": "file",
    "CHANGE-NOTE": "change-note",
    "ENVIRONMENT": "environment",
    "SPEC-TARGET": "spec-target",
    "EXPORT-FIG": "export-fig",
    "LOG": "log",
    "DATA": "data",
    "CRITERION": "criterion",
}

ONLY_PROGRAM = [CONST["DATA"], CONST["LOG"]]


# Logger Template in system
LOGGER_TEMPLATE = {
    "usage": "PROJECTION-LENS",
    "engine": "pyzdde",
    "template": {
        "PROJECTION-LENS": {
            CONST["TRACKFILE"]: {"file": None},
            CONST["CHANGE-NOTE"]: {"target": None, "method": None, "summary": None},
            CONST["ENVIRONMENT"]: {
                "sensor": None,
                "format-v": None,
                "format-h": None,
                "pixel-size": None,
                "cra-imh": None,
                "process-type": None,
            },
            CONST["DATA"]: {
                "op-dfov": None,
                "op-hfov": None,
                "op-vfov": None,
                "me-dfov": None,
                "me-hfov": None,
                "me-vfov": None,
                "mtfs": None,
                "mtft": None,
                "mtfs-center": None,
                "mtfs-middle": None,
                "mtfs-outer": None,
                "mtfs-mic": None,
                "mtft-center": None,
                "mtft-middle": None,
                "mtft-outer": None,
                "mtft-mic": None,
                "cra": None,
                "wfno": None,
                "fno": None,
                "ri": None,
                "eflm": None,
                "efl": None,
                "op-ttl": None,
                "op-dist": None,
                "tv-dist": None,
                "lacl-F11": None,
                "lacl-F12": None,
                "fcgs": None,
                "aper-pos": None,
                "tir": None,
            },
            CONST["EXPORT-FIG"]: {
                "rel": False,
                "tfm": False,
                "mtf": False,
                "fcd-tan": False,
                "fcg-ftheta": False,
                "spt": False,
            },
            CONST["SPEC-TARGET"]: {
                "op-dfov": None,
                "fno": None,
                "cra": None,
                "max-cra": None,
                "ri": None,
                "focal-depth": None,
            },
            CONST["CRITERION"]: {
                "wfno": 0.02,
                "op-dfov": 0.5,
                "cra-upper": 3,
                "cra-lower": -3,
                "aper-pos-lower": 0.01,
                "aper-pos-upper": 0.03,
                "op-dist": 1,
                "tv-dist": 0.5,
                "fcgs": 0.005,
                "lacl-F11": 1.116,
                "lacl-F12": 2.232,
                "mtf-center": 0.75,
                "mtf-middle": 0.6,
                "mtf-outer": 0.6,
                "mtf-mic": 0.2,
                "tir": 35,
            },
        },
        "COSTUME": {
            "file": {},
            "change-note": {},
            "environment": {},
            "data": {},
            "criterion": {},
        },
    },
}
