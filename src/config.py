from pathlib import Path
from pathlib import PurePath

# Installed file
INSTALLED_FOLDER = PurePath("D:/Code/Python_Code/optical_git")
USR_CONFIG = INSTALLED_FOLDER.joinpath("usr_config.json")

# The constant variable in system
CONST = {
    "TRACKFILE": "file",
    "CHANGE_NOTE": "change_note",
    "ENVIRONMENT": "environment",
    "SPEC_TARGET": "spec_target",
    "LOG": "log",
    "DATA": "data",
    "CRITERION": "criterion",
}

ONLY_PROGRAM = [CONST["DATA"], CONST["LOG"]]


# Logger Template in system
LOGGER_TEMPLATE = {
    "usage": "PROJECTION_LENS",
    "engine": "pyzdde",
    "template": {
        "PROJECTION_LENS": {
            CONST["TRACKFILE"]: {"file": None},
            CONST["CHANGE_NOTE"]: {"target": None, "method": None, "summary": None},
            CONST["ENVIRONMENT"]: {
                "sensor": None,
                "format_v": None,
                "format_h": None,
                "pixel_size": None,
                "cra_imh": None,
                "process_type": None,
            },
            CONST["DATA"]: {
                "op-dfov": None,
                "op-hfov": None,
                "op-vfov": None,
                "op-ttl": None,
                "ri": None,
                "mtfs": None,
                "mtft": None,
                "cra": None,
                "op-dist": None,
                "tv-dist": None,
                "lacl-F11": None,
                "lacl-F12": None,
                "wfno": None,
                "fno": None,
            },
            CONST["SPEC_TARGET"]: {
                "op-dfov": None,
                "fno": None,
                "cra0": None,
                "cra1": None,
                "cra2": None,
                "cra3": None,
                "cra4": None,
                "cra5": None,
                "cra6": None,
                "cra7": None,
                "cra8": None,
                "cra9": None,
                "cra10": None,
                "max_cra": None,
                "ri": None,
                "focal-depth": None,
            },
            CONST["CRITERION"]: {
                "wfno": 0.02,
                "op-dfov": 0.5,
                "cra-upper": 3,
                "cra-lower": -3,
                "op-dist": 1,
                "tv-dist": 0.5,
                "fcgs": 0.005,
                "lacl-F11": 1.116,
                "lacl-F12": 2.232,
                "mtf-center": 0.75,
                "mtf-middle": 0.6,
                "mtf-outer": 0.6,
                "mtf-mic": 0.2,
            },
        },
        "COSTUME": {
            "file": {},
            "change_note": {},
            "environment": {},
            "data": {},
            "criterion": {},
        },
    },
}
