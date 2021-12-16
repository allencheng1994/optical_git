from pathlib import Path
from pathlib import PurePath

# Installed file
INSTALLED_FOLDER = PurePath("D:/Code/Python_Code/optical_git")
USR_CONFIG = INSTALLED_FOLDER.joinpath("usr_config.json")
CONFIG_FOLDER = INSTALLED_FOLDER.joinpath("config/")
TEMP_FOLDER = INSTALLED_FOLDER.joinpath("temp/")

# The constant variable in system
CONST = {
    "OPTICAL-GIT": ".optical-git",
    "OPTICAL-GIT-TEMP": "temp",
    "TRACKFILE": "file",
    "CHANGE-NOTE": "change-note",
    "ENVIRONMENT": "environment",
    "SPEC-TARGET": "spec-target",
    "EXPORT-FIG": "export-fig",
    "LOG": "log",
    "DATA": "data",
    "CRITERION": "criterion",
    "YIELD_SETTING": "yield",
}

ONLY_PROGRAM = [CONST["DATA"], CONST["LOG"]]


CODEV_LENS_SETTING_TEMPLATE = {
    "file": "",
    "plasticprv": "C:/CVUSER/plasticprv.seq",
    "mode": "normal",
    "material": [],
    "mid": 0,
    "imh": 0,
    "line_pair": 0,
    "field_sym": True,
    "field_gen": [
        0,
        0.3,
        0.6,
        0.8,
        0.9,
        1,
    ],
    "field": [
        0,
        0.3,
        0.6,
        0.8,
        0.9,
        1,
        -0.3,
        -0.6,
        -0.8,
        -0.9,
        -1,
        0.3,
        0.6,
        0.8,
        0.9,
        1,
        -0.3,
        -0.6,
        -0.8,
        -0.9,
        -1,
    ],
    "wavelength": [650, 610, 555, 510, 470],
    "wavelength_weight": [107, 503, 1000, 503, 91],
    "wavelength_line_color": ["RED", "RED", "CYA", "BLU", "MAG"],
}


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
                "yield-mode": "normal",
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
                "fcd-ftheta": False,
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
                "boundary-list": [0.67, 0.47, 0, 0.38, 0, 0, 0.47, 0, 0.38, 0, 0],
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
