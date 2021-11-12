from pathlib import Path
from pathlib import PurePath

# Installed file
INSTALLED_FOLDER = PurePath('D:/Code/Python_Code/optical_git')
USR_CONFIG = INSTALLED_FOLDER.joinpath("usr_config.json")

# The constant variable in system
CHANGE_NOTE = "change_note"
ENVIRONMENT = "environment"
LOG = "log"
DATA = "data"

ONLY_PROGRAM = [DATA, LOG]
EXTRACTING_CODE = ["dfov", "hfov", "vfov", "mtfs", "mtft", "cra", "etva", "ctva"]
SETTING_CODE = ['fld']


# Logger Template in system
PROJECTION_LENS_BASIC_TEMPLATE = {
    CHANGE_NOTE: {"target": None, "method": None, "summary": None},
    ENVIRONMENT: {
        "sensor": None,
        "format_v": None,
        "format_h": None,
        "pixel_size": None,
        "cra_imh": None,
    },
    DATA: {
        "dfov": None,
        "hfov": None,
        "vfov": None,
        "mtfs": None,
        "mtft": None,
        "cra": None,
    },
}
