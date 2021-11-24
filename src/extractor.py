import json
import math
from ZOS_DDE.zemax_pyzdde import Zemax14
from pathlib import Path
from config import EXTRACTING_CODE
from common import *


class ProjectionLensEnvironment(object):
    def __init__(self):
        repo = find_optical_repo_path()
        data = load_json_data(repo.joinpath("environment.json"))

        self.__vfov_nominal = data["format_v"] / math.sqrt(
            data["format_h"] ** 2 + data["format_v"] ** 2
        )

        self.__hfov_nominal = data["format_h"] / math.sqrt(
            data["format_h"] ** 2 + data["format_v"] ** 2
        )
        self.__line_pair_q = 1000 / data[""]
        self.__imh = (
            math.sqrt(data["format_h"] ** 2 + data["format_v"] ** 2)
            * data["pixel_size"]
            / 1000
            / 2
        )
        self.__cra_imh = data['cra_imh'] if data['cra_imh'] != None else self.__imh


class ZDDEProjectionLensDataExtractor(ProjectionLensEnvironment):
    def __init__(self, zfile):
        self.__zfile = zfile
        super(ZDDEProjectionLensDataExtractor, self).__init__()
        self.__system_info = self.__zfile.zGetSystem()
        self.__primary_wave_id = self.__zfile.zGetWave(0)[0]
        self.__nsur = self.__system_info[0]

        cons_tuple = self.__zfile.zGetConfig()
        for i in range(cons_tuple[1]):
            self.__zfile.zDeleteConfig(1)
        for i in range(cons_tuple[2]):
            self.__zfile.zDeleteMCO(1)

        self.__set_default_field()
        self.__set_default_wavelength()

    def __set_default_field(self):
        self.__zfile.zSetField(0, 3, 11, 0)
        for i in range(11):
            self.__zfile.zSetField(i + 1, 0, self.__imh * i * 0.1, 1)
        self.__zfile.zSetVig()
        self.__zfile.zGetUpdate()

    def __set_particular_height(self, height):
        self.__zfile.zSetField(0, 3, 12, 0)
        for i in range(11):
            self.__zfile.zSetField(i + 1, 0, self.__imh * i * 0.1, 1)
        self.__zfile.zSetField(12, 0, height, 1)
        self.__zfile.zSetVig()
        self.__zfile.zGetUpdate()

    def __set_default_wavelength(self):
        self.__zfile.zSetWave(
            0, len(self.__wavelength) // 2 + 1, len(self.__wavelength)
        )
        self.__zfile.zSetVig()
        self.__zfile.zGetUpdate()

    def __get_fov(self, nominal):
        return (
            self.__zfile.zOperandValue(
                "RAID", 1, self.__primary_wave_id, 0, nominal, 0, 0
            )
            * 2
        )

    def __get_mtfs(self, line_pair, field):
        return self.__zfile.zOperandValue("MTFS", 2, 0, field, line_pair, 0, 0)

    def __get_mtft(self, line_pair, field):
        return self.__zfile.zOperandValue("MTFT", 2, 0, field, line_pair, 0, 0)

    def __get_lens_cra(self, sensor_imh, n=10):
        for i in range(11):
            self.__zfile.zSetField(i + 1, 0, sensor_imh * i * 0.1, 1)
        self.__zfile.zSetVig()
        self.__zfile.zGetUpdate()

        cra = [
            self.__zfile.zOperandValue(
                "RAID", self.__nsur, self.__primary_wave_id, 0, i * 1 / n, 0, 0
            )
            for i in range(n + 1)
        ]

        self.__set_default_field()
        return cra

    def extract_data(self, operand_code):
        data = {
            'dfov': self.__get_fov(1),
            'hfov': self.__get_fov(self.__hfov_nominal),
            'vfov': self.__get_fov(self.__vfov_nominal),
            'mtfs': [self.__get_mtfs(self.__line_pair_q, i) for i in range(11)],
            'mtft': [self.__get_mtft(self.__line_pair_q, i) for i in range(11)],
            'cra': [self.__get_lens_cra(self.__cra_imh)],
        }
        return data.get(operand_code)


if __name__ == '__main__':
    pass
