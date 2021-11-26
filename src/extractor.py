import json
import math
from ZOS_DDE.zemax_pyzdde import Zemax14
from .common import load_json_data
from .common import find_optical_repo_path
from .config import CONST


class ProjectionLensEnvironment:
    """
    This Object is an instance that is used to initialize the environment settings of
    projecttion lens.
    """

    def __init__(self):
        repo = find_optical_repo_path()
        data = load_json_data(repo.joinpath(CONST["ENVIRONMENT"] + ".json"))
        self._format_v = data["format_v"]
        self._format_h = data["format_h"]
        self._pixel_size = data["pixel_size"]
        self._type = data["process_type"].lower()

        self._imh = (
            math.sqrt(self._format_h ** 2 + self._format_v ** 2)
            * self._pixel_size
            / 1000
            / 2
        )
        self._cra_imh = data["cra_imh"] if data["cra_imh"] else self._imh

        if self._type == "cob":
            self._half_mic = self._imh + 0.1
        elif self._type == "csp":
            self._half_mic = self._imh + 0.15
        else:
            self._half_mic = 0

        self._vfov_nominal = self._format_v / math.sqrt(
            self._format_h ** 2 + self._format_v ** 2
        )

        self._hfov_nominal = self._format_h / math.sqrt(
            self._format_h ** 2 + self._format_v ** 2
        )
        self._line_pair_q = 1000 / self._pixel_size / 4 / 2


class ZDDEProjectionLensDataExtractor(ProjectionLensEnvironment):
    """
    To use this case, you need to create a link from pyzdde and return the channel.
    Then, you need to input the channel into the argument zfile.
    """

    def __init__(self, zfile):
        self.__zfile = zfile
        ProjectionLensEnvironment.__init__(self)
        self.__system_info = self.__zfile.zGetSystem()
        self.__primary_wave_id = self.__zfile.zGetWave(0)[0]
        self.__nwave = self.__zfile.zGetSystemProperty(201)
        self.__nsur = self.__system_info[0]
        self.__nfield = 11

        cons_tuple = self.__zfile.zGetConfig()
        for _ in range(cons_tuple[1]):
            self.__zfile.zDeleteConfig(1)
        for _ in range(cons_tuple[2]):
            self.__zfile.zDeleteMCO(1)

        self.__set_default_field()

    def __set_default_field(self):
        self.__zfile.zSetField(0, 3, self.__nfield, 0)
        for i in range(self.__nfield):
            self.__zfile.zSetField(i + 1, 0, self._imh * i * 0.1, 1)
        self.__zfile.zSetVig()
        self.__zfile.zGetUpdate()

    def __set_particular_height(self, height):
        self.__zfile.zSetField(0, 3, self.__nfield + 1, 0)
        for i in range(self.__nfield):
            self.__zfile.zSetField(i + 1, 0, self._imh * i * 0.1, 1)
        self.__zfile.zSetField(self.__nfield + 1, 0, height, 1)
        self.__zfile.zSetVig()
        self.__zfile.zGetUpdate()

    def __get_fov(self, nominal):
        return (
            self.__zfile.zOperandValue(
                "RAID", 1, self.__primary_wave_id, 0, nominal, 0, 0
            )
            * 2
        )

    def __get_fov_particular_height(self, nominal, height):
        self.__set_particular_height(height)
        result = (
            self.__zfile.zOperandValue(
                "RAID", nominal, self.__primary_wave_id, 0, nominal, 0, 0
            )
            * 2
        )
        self.__set_default_field()
        return result

    def __get_mtfs(self, line_pair, field):
        return self.__zfile.zOperandValue("MTFS", 2, 0, field, line_pair, 0, 0)

    def __get_mtft(self, line_pair, field):
        return self.__zfile.zOperandValue("MTFT", 2, 0, field, line_pair, 0, 0)

    def __get_lens_cra(self, sensor_imh, num=10):
        for i in range(num + 1):
            self.__zfile.zSetField(i + 1, 0, sensor_imh * i * 0.1, 1)
        self.__zfile.zSetVig()
        self.__zfile.zGetUpdate()

        cra = [
            self.__zfile.zOperandValue(
                "RAID", self.__nsur, self.__primary_wave_id, 0, i * 1 / num, 0, 0
            )
            for i in range(num + 1)
        ]

        self.__set_default_field()
        return cra

    def __get_fno(self):
        return self.__zfile.zGetSystemAper()[2]

    def __get_wfno(self):
        return self.__zfile.zOperandValue("WFNO", 0, 0, 0, 0, 0, 0)

    def __get_ri(self):
        return self.__zfile.zOperandValue(
            "RELI", 20, self.__primary_wave_id, self.__nfield, 1, 0, 0
        )

    def __get_eflm(self):
        objy = self.__zfile.zOperandValue(
            "REAY", 0, self.__primary_wave_id, 0, 0.001, 0, 0
        )
        imhy = self.__zfile.zOperandValue(
            "REAY", self.__nsur, self.__primary_wave_id, 0, 0.001, 0, 0
        )
        obj_dist = self.__zfile.zOperandValue("TTHI", 0, 0, 0, 0, 0, 0)
        return abs(imhy / objy * obj_dist)

    def __get_efl(self):
        return self.__zfile.zOperandValue("EFFL", 0, self.__primary_wave_id, 0, 0, 0, 0)

    def __get_op_ttl(self):
        return self.__zfile.zOperandValue("TTHI", 2, self.__nsur - 1, 0, 0, 0, 0)

    def __get_op_dist(self):
        data = [
            abs(self.__zfile.zOperandValue("DISG", 1, 3, 0, i / 100, 0, 0))
            for i in range(101)
        ]
        return max(data)

    def __get_tv_dist(self):
        data = [
            self.__zfile.zOperandValue("DISG", 1, 3, 0, i / 100, 0, 0)
            for i in range(101)
        ]
        return abs(max(data) - min(data))

    def __get_lacl_f11(self):
        data = [
            abs(
                self.__zfile.zOperandValue(
                    "REAY", self.__nsur, self.__primary_wave_id, 0, 1, 0, 0
                )
                - self.__zfile.zOperandValue("REAY", self.__nsur, i, 0, 1, 0, 0)
            )
            for i in range(1, self.__nwave + 1)
        ]
        return max(data)

    def __get_lacl_f12(self):
        self.__set_particular_height(self._half_mic)
        result = self.__get_lacl_f11()
        self.__set_default_field()
        return result

    def __get_fcgs(self):
        return self.__zfile.zOperandValue("FCGS", 0, 3, 0, 0, 0, 0)

    def extract(self, operand_code):
        """
        Give the operand code in it. The supported operand code are following:
            'op-dfov': extract the optical field of view in diagonal direction.
            'op-hfov': extract the optical field of view in horizontal direction.
            'op-vfov': extract the optical field of view in vertical direction.

            'me-dfov': extract the mechanical field of view in diagonal direction.
            'me-hfov': extract the mechanical field of view in horizontal direction.
            'me-vfov': extract the mechanical field of view in vertical direction.

            'mtfs': extract the mtf in sagital direction.
            'mtft': extract the mtf in tangential direction.
            'cra': extract the chief ray angle.
            'elfm': extract the effective focal length using magnification method to calculate.
            'efl': extraact the effective focal length which calculated by the operand, EFFL, in Zemax.
            'op-ttl': extract total length of the optical system.
            'op-dist': extract the geometric optical distortion.
            'tv-dist': extract the TV distortion.
            'lacl-f11': extract the lateral color at 1.0 field.
            'lacl-f12': extract teh lateral color at 1.1 field.
            'fno': get the f number of the system.
            'wfno': get the working f number of the system.
        """
        print(f"Extracting data: {operand_code}")
        operand_code = operand_code.lower()
        try:
            data = {
                "op-dfov": self.__get_fov(1),
                "op-hfov": self.__get_fov(self._hfov_nominal),
                "op-vfov": self.__get_fov(self._vfov_nominal),
                "me-dfov": self.__get_fov_particular_height(1, self._imh),
                "me-hfov": self.__get_fov_particular_height(
                    self._hfov_nominal, self._imh
                ),
                "me-vfov": self.__get_fov_particular_height(
                    self._vfov_nominal, self._imh
                ),
                "mtfs": [
                    self.__get_mtfs(self._line_pair_q, i + 1)
                    for i in range(self.__nfield)
                ],
                "mtft": [
                    self.__get_mtft(self._line_pair_q, i + 1)
                    for i in range(self.__nfield)
                ],
                "cra": self.__get_lens_cra(self._cra_imh),
                "fno": self.__get_fno(),
                "wfno": self.__get_wfno(),
                "ri": self.__get_ri(),
                "eflm": self.__get_eflm(),
                "efl": self.__get_efl(),
                "op-ttl": self.__get_op_ttl(),
                "op-dist": self.__get_op_dist(),
                "tv-dist": self.__get_tv_dist(),
                "lacl-f11": self.__get_lacl_f11(),
                "lacl-f12": self.__get_lacl_f12(),
                "fcgs": self.__get_fcgs(),
            }
            result = data[operand_code]
        except KeyError:
            print(f"The operand code, {operand_code}, is not supported.")
            result = None
        return result


def log_data(file, refresh=False):
    repo = find_optical_repo_path()
    json_file = repo.joinpath(CONST["DATA"] + ".json")
    data = load_json_data(json_file)

    if refresh:
        extract_operand_code = data.keys()
    else:
        extract_operand_code = [
            operand_code for operand_code in data if data[operand_code] is None
        ]

    with Zemax14(file) as zfile:
        data_extractor = ZDDEProjectionLensDataExtractor(zfile)
        for operand_code in extract_operand_code:
            data[operand_code] = data_extractor.extract(operand_code)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f)


if __name__ == "__main__":
    pass
