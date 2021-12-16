import numpy as np
import math
from .config import CODEV_LENS_SETTING_TEMPLATE
from .common import CodeVStandaloneApplication
from .common import load_json_data
from .lens_unit import LensUnit
from .CVcmd import *


def extract_yield_data(lens_config, yield_config):
    cvapi = CodeVStandaloneApplication()
    cvapp = cvapi.TheApplication
    cv_classified = CV_CLASSIFIED(cvapp)

    cv_classified.SystemFile.inputZMX(lens_config["file"])
    cv_classified.SystemFile.inputPlastic(lens_config["plasticprv"])

    lens_unit = LensUnit(len(lens_config["material"]), mid=lens_config["mid"])
    material_surface = lens_unit.get_materialID()
    for i, material in enumerate(lens_config["material"]):
        cv_classified.Material.setGL1(material_surface[i], material)

    cv_classified.Field.setFieldTypeRIH()

    cv_classified.Wavelength.setWave(
        lens_config["wavelength"],
        lens_config["wavelength_weight"],
        lens_config["wavelength_line_color"],
    )

    for i, fld in enumerate(lens_config["field"]):
        if i != 0:
            cv_classified.Field.insertField(i)
            cv_classified.Field.setIMH_RIH(i + 1, fld * lens_config["imh"])

    cv_classified.Field.setCRA()
    cv_classified.Tolerance.clear()

    for i, surface in enumerate(lens_unit.get_surfaceID()):
        cv_classified.Tolerance.dlx(surface, yield_config["DL"][i])
        cv_classified.Tolerance.dly(surface, yield_config["DL"][i])
        cv_classified.Tolerance.til(surface, yield_config["DL"][i])
        cv_classified.Tolerance.dls(surface, yield_config["DL"][i])
        cv_classified.Tolerance.dlt(surface, yield_config["DL"][i])

    for i, part in enumerate(lens_unit.get_partID()):
        cv_classified.Tolerance.dsx(part, yield_config["DS"][i])
        cv_classified.Tolerance.dsy(part, yield_config["DS"][i])
        cv_classified.Tolerance.btx(part, yield_config["BT"][i])
        cv_classified.Tolerance.bty(part, yield_config["BT"][i])

    cv_classified.Compensator.dlt("SI", 0.2)
    cv_classified.Tolerance.torPTIC(lens_config["line_pair"])
    cv_classified.Field.setWeight(1, 9999)
    cv_classified.Plot.plotGrid(runs=1000, upper=1, lower=0, step=0.1)

    cv_classified.Buffer.wmc("B1")
    cv_classified.Buffer.wpb("B1")

    cvapp.command("SNS YES")
    cvapp.command("DST Y")
    cvapp.command("GO")
    cvapp.command("DEL TOL SA")

    result = {
        "azimuth": np.zeros(21),
        "weight": np.zeros(21),
        "mtf_design": np.zeros(21),
        "mtf_tol": np.zeros(21),
        "delta": np.zeros(21),
        "mtf_yield": np.zeros(21000),
    }

    result["azimuth"] = cvapp.BufferToArray(16, 36, 6, 6, 1, result["azimuth"])[-1]
    result["weight"] = cvapp.BufferToArray(16, 36, 7, 7, 1, result["weight"])[-1]
    result["mtf_design"] = cvapp.BufferToArray(16, 36, 8, 8, 1, result["mtf_design"])[
        -1
    ]
    result["mtf_tol"] = cvapp.BufferToArray(16, 36, 12, 12, 1, result["mtf_tol"])[-1]
    result["delta"] = cvapp.BufferToArray(16, 36, 18, 18, 1, result["delta"])[-1]
    result["mtf_yield"] = cvapp.BufferToArray(42, 21041, 5, 5, 1, result["mtf_yield"])[
        -1
    ]

    return result


def __count_larger(num_list, boundary):
    return sum(num >= boundary for num in num_list)


def __arrange_mtf(mtf_result_codev, sep_part=21):
    result = [[] for sep in range(sep_part)]
    i = 0
    for mtf in mtf_result_codev:
        result[i].append(mtf)
        i += 1
        if i == sep_part:
            i = 0
    return result


def __arrange_mtf_symmetry(arranged_mtf):
    result = []
    center, *need_arranged = arranged_mtf
    result.append(center)

    tan_part = need_arranged[: int(len(need_arranged) / 2)]
    sag_part = need_arranged[int(len(need_arranged) / 2) :]

    tan_positive = tan_part[: int(len(tan_part) / 2)]
    tan_negative = tan_part[int(len(tan_part) / 2) :]

    sag_positive = sag_part[: int(len(sag_part) / 2)]
    sag_negative = sag_part[int(len(sag_part) / 2) :]

    for positive, negative in zip(tan_positive, tan_negative):
        new_tan = [min(mtf_1, mtf2) for mtf_1, mtf2 in zip(positive, negative)]
        result.append(new_tan)

    for positive, negative in zip(sag_positive, sag_negative):
        new_sag = [min(mtf_1, mtf2) for mtf_1, mtf2 in zip(positive, negative)]
        result.append(new_sag)

    return result


def cal_yield(mtf_group, boundary_list):
    result = []
    for mtf_list, boundary in zip(mtf_group, boundary_list):
        result.append(__count_larger(mtf_list, boundary))
    return result


def go_tolerancing(setting):
    lens_config = lens_settings
    yield_config = load_json_data()
    result = extract_yield_data(lens_config, yield_config)

    arranged_mtf = __arrange_mtf(result.get("mtf_yield"), 21)
    sym = __arrange_mtf_symmetry(arranged_mtf)

    sample = 1000
    for boundary in boundary_list:
        result = cal_yield(sym, boundary)
        percentage_list = [num / sample for num in result]
    return percentage_list


if __name__ == "__main__":
    pass
