import json
import math
from ZOS_DDE.zemax_pyzdde import Zemax14
from .common import load_json_data
from .common import find_optical_repo_path
from .config import CONST
from .config import CONFIG_FOLDER


class ProjectionLensEnvironment:
    """
    This Object is an instance that is used to initialize the environment settings of
    projecttion lens.
    """

    def __init__(self):
        repo = find_optical_repo_path()
        data = load_json_data(repo.joinpath(CONST["ENVIRONMENT"] + ".json"))
        self._format_v = data["format-v"]
        self._format_h = data["format-h"]
        self._pixel_size = data["pixel-size"]
        self._type = data["process-type"].lower()

        self._imh = (
            math.sqrt(self._format_h ** 2 + self._format_v ** 2)
            * self._pixel_size
            / 1000
            / 2
        )
        self._cra_imh = data["cra-imh"] if data.get("cra-imh") != None else self._imh

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


class CODEVProjectionLensDataExtractor(ProjectionLensEnvironment):
    """
    To use this class, you need to create a link between python and CodeV
    """

    def __init__(self, channel):
        self.__zfile = channel
        ProjectionLensEnvironment.__init__(self)
        self.__primary_wave_id = None
        self.__nwave = None
        self.__nsur = None


class ZOSProjectionLensDataExtractor(ProjectionLensEnvironment):
    """
    To use this class, you need to create a link from ZOS-API and return the channel.
    Then, you need to input the channel into the argument zfile.
    """

    def __init__(self, channel):
        self.__zfile = channel
        ProjectionLensEnvironment.__init__(self)
        self.__primary_wave_id = None
        self.__nwave = None
        self.__nsur = None


class ZDDEProjectionLensDataExtractor(ProjectionLensEnvironment):
    """
    To use this class, you need to create a link from pyzdde and return the channel.
    Then, you need to input the channel into the argument zfile.
    """

    def __init__(self, channel):
        self.__zfile = channel
        ProjectionLensEnvironment.__init__(self)
        self.__system_info = self.__zfile.zGetSystem()
        self.__nsur = self.__system_info[0]
        self.__primary_wave_id = self.__zfile.zGetWave(0)[0]
        self.__nwave = self.__zfile.zGetSystemProperty(201)
        self.__nfield = 11

        self.__rm_coordinate_break()

        cons_tuple = self.__zfile.zGetConfig()
        for _ in range(cons_tuple[1]):
            self.__zfile.zDeleteConfig(1)
        for _ in range(cons_tuple[2]):
            self.__zfile.zDeleteMCO(1)

        self.__set_default_field()

    def __rm_coordinate_break(self):
        coord_id = []
        for surf_num in range(1, self.__nsur + 1):
            surf_type = self.__zfile.zGetSurfaceData(surf_num, 0)
            if surf_type == "COORDBRK":
                coord_id.append(surf_num)
        coord_id.reverse()

        for coord in coord_id:
            self.__zfile.zDeleteSurface(coord)
        self.__system_info = self.__zfile.zGetSystem()
        self.__nsur = self.__system_info[0]

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

    def _get_fov(self, nominal):
        return (
            self.__zfile.zOperandValue(
                "RAID", 1, self.__primary_wave_id, 0, nominal, 0, 0
            )
            * 2
        )

    def _get_op_dfov(self):
        return self._get_fov(1)

    def _get_op_hfov(self):
        return self._get_fov(self._hfov_nominal)

    def _get_op_vfov(self):
        return self._get_fov(self._vfov_nominal)

    def _get_fov_particular_height(self, nominal, height):
        self.__set_particular_height(height)
        result = (
            self.__zfile.zOperandValue(
                "RAID", nominal, self.__primary_wave_id, 0, nominal, 0, 0
            )
            * 2
        )
        self.__set_default_field()
        return result

    def _get_me_dfov(self):
        return self._get_fov_particular_height(1, self._half_mic)

    def _get_me_hfov(self):
        return self._get_fov_particular_height(self._hfov_nominal, self._half_mic)

    def _get_me_vfov(self):
        return self._get_fov_particular_height(self._vfov_nominal, self._half_mic)

    def _get_mtfs(self, line_pair, field):
        return self.__zfile.zOperandValue("MTFS", 2, 0, field, line_pair, 0, 0)

    def _get_mtfs_whole_default(self):
        return [self._get_mtfs(self._line_pair_q, i + 1) for i in range(self.__nfield)]

    def _get_mtfs_center_default(self):
        return self._get_mtfs(self._line_pair_q, 1)

    def _get_mtfs_middle_default(self):
        return self._get_mtfs(self._line_pair_q, 4)

    def _get_mtfs_outer_default(self):
        return self._get_mtfs(self._line_pair_q, 9)

    def _get_mtfs_particular_height(self, line_pair, height):
        self.__set_particular_height(height)
        result = self.__zfile.zOperandValue("MTFS", 2, 0, 12, line_pair, 0, 0)
        self.__set_default_field()
        return result

    def _get_mtfs_mic_default(self):
        return self._get_mtfs_particular_height(self._line_pair_q, self._half_mic)

    def _get_mtft(self, line_pair, field):
        return self.__zfile.zOperandValue("MTFT", 2, 0, field, line_pair, 0, 0)

    def _get_mtft_whole_default(self):
        return [self._get_mtft(self._line_pair_q, i + 1) for i in range(self.__nfield)]

    def _get_mtft_center_default(self):
        return self._get_mtft(self._line_pair_q, 1)

    def _get_mtft_middle_default(self):
        return self._get_mtft(self._line_pair_q, 4)

    def _get_mtft_outer_default(self):
        return self._get_mtft(self._line_pair_q, 9)

    def _get_mtft_particular_height(self, line_pair, height):
        self.__set_particular_height(height)
        result = self.__zfile.zOperandValue("MTFT", 2, 0, 12, line_pair, 0, 0)
        self.__set_default_field()
        return result

    def _get_mtft_mic_default(self):
        return self._get_mtft_particular_height(self._line_pair_q, self._half_mic)

    def _get_lens_cra(self, sensor_imh, num=10):
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

    def _get_lens_cra_default(self):
        return self._get_lens_cra(self._cra_imh)

    def _get_fno(self):
        return self.__zfile.zGetSystemAper()[2]

    def _get_wfno(self):
        return self.__zfile.zOperandValue("WFNO", 0, 0, 0, 0, 0, 0)

    def _get_ri(self):
        return self.__zfile.zOperandValue(
            "RELI", 20, self.__primary_wave_id, self.__nfield, 1, 0, 0
        )

    def _get_eflm(self):
        objy = self.__zfile.zOperandValue(
            "REAY", 0, self.__primary_wave_id, 0, 0.001, 0, 0
        )
        imhy = self.__zfile.zOperandValue(
            "REAY", self.__nsur, self.__primary_wave_id, 0, 0.001, 0, 0
        )
        obj_dist = self.__zfile.zOperandValue("TTHI", 0, 0, 0, 0, 0, 0)
        return abs(imhy / objy * obj_dist)

    def _get_efl(self):
        return self.__zfile.zOperandValue("EFFL", 0, self.__primary_wave_id, 0, 0, 0, 0)

    def _get_op_ttl(self):
        return self.__zfile.zOperandValue("TTHI", 2, self.__nsur - 1, 0, 0, 0, 0)

    def _get_op_dist(self):
        data = [
            abs(self.__zfile.zOperandValue("DISG", 1, 3, 0, i / 100, 0, 0))
            for i in range(101)
        ]
        return max(data)

    def _get_tv_dist(self):
        data = [
            self.__zfile.zOperandValue("DISG", 1, 3, 0, i / 100, 0, 0)
            for i in range(101)
        ]
        return abs(max(data) - min(data))

    def _get_lacl_f11(self):
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

    def _get_lacl_f12(self):
        self.__set_particular_height(self._half_mic)
        result = self._get_lacl_f11()
        self.__set_default_field()
        return result

    def _get_fcgs(self):
        return self.__zfile.zOperandValue("FCGS", 0, 3, 0, 0, 0, 0)

    def _get_stop_p1_edge(self):
        return self.__zfile.zOperandValue("ETVA", 1, 0, 0, 0, 0, 0)

    def _get_reflected_angle(self):
        self.__set_particular_height(self._half_mic)
        py_list = [0.9, 0.92, 0.94, 0.95, 0.98, 0.99, 1]
        result = [
            self.__zfile.zOperandValue("ZPLM", 99, 0, 0, 1, 0, py) for py in py_list
        ]
        self.__set_default_field()
        for py in py_list:
            result.append(self.__zfile.zOperandValue("ZPLM", 99, 0, 0, 1, 0, py))
        return result

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
                center 0F, middle 0.3F, outer 0.8F, mic 1.1F
\
            'cra': extract the chief ray angle.
            'wfno': get the working f number of the system.
            'fno': get the f number of the system.
            
            'ri': get the relative illumination on 1.0F

            'elfm': extract the effective focal length using magnification method to calculate.
            'efl': extraact the effective focal length which calculated by the operand, EFFL, in Zemax.
            
            'op-ttl': extract total length of the optical system.
            
            'op-dist': extract the geometric optical distortion.
            'tv-dist': extract the TV distortion.
            
            'lacl-f11': extract the lateral color at 1.0 field.
            'lacl-f12': extract teh lateral color at 1.1 field.
            
            'fcgs': get the field curvature in sagital direction at center.

            'aper-pos': get the distance between the edge of the stop and the first lens in your system.
            
            'tir': extract the reflected angle of the last lens in the system.

        """
        print(f"Extracting data: {operand_code}")
        operand_code = operand_code.lower()
        data = {
            "op-dfov": self._get_op_dfov,
            "op-hfov": self._get_op_hfov,
            "op-vfov": self._get_op_vfov,
            "me-dfov": self._get_me_dfov,
            "me-hfov": self._get_me_hfov,
            "me-vfov": self._get_me_vfov,
            "mtfs": self._get_mtfs_whole_default,
            "mtft": self._get_mtft_whole_default,
            "mtfs-center": self._get_mtfs_center_default,
            "mtfs-middle": self._get_mtfs_middle_default,
            "mtfs-outer": self._get_mtfs_outer_default,
            "mtfs-mic": self._get_mtfs_mic_default,
            "mtft-center": self._get_mtft_center_default,
            "mtft-middle": self._get_mtft_middle_default,
            "mtft-outer": self._get_mtft_outer_default,
            "mtft-mic": self._get_mtft_mic_default,
            "cra": self._get_lens_cra_default,
            "fno": self._get_fno,
            "wfno": self._get_wfno,
            "ri": self._get_ri,
            "eflm": self._get_eflm,
            "efl": self._get_efl,
            "op-ttl": self._get_op_ttl,
            "op-dist": self._get_op_dist,
            "tv-dist": self._get_tv_dist,
            "lacl-f11": self._get_lacl_f11,
            "lacl-f12": self._get_lacl_f12,
            "fcgs": self._get_fcgs,
            "aper-pos": self._get_stop_p1_edge,
            "tir": self._get_reflected_angle,
        }
        result = data.get(operand_code)()
        if result is None:
            print(
                f"The operand code, {operand_code}, is not supported by"
                " ZDDEProjectionLensDataExtractor."
            )
        return result

    def _export_figure_ri(self, save_path):
        self.__zfile.zGetMetaFile(save_path.joinpath("rel.wmf"), "Rel")

    def _export_figure_mtfvslp(self, save_path, line_pair):
        self.__zfile.zSetField(0, 3, 4, 0)
        self.__zfile.zSetField(1, 0, 0, 1)
        self.__zfile.zSetField(2, 0, 0.6 * self._imh, 1)
        self.__zfile.zSetField(3, 0, 0.8 * self._imh, 1)
        self.__zfile.zSetField(4, 0, self._imh, 1)
        self.__zfile.zModifySettings(
            save_path.joinpath("tmp.CFG"), "MTF_MAXF", line_pair
        )
        self.__zfile.zGetMetaFile(
            save_path.joinpath("mtf.wmf"), "Mtf", save_path.joinpath("tmp.CFG"), 1
        )
        self.__set_default_field()

    def _export_figure_mtfvslp_default(self, save_path):
        self._export_figure_mtfvslp(save_path, self._line_pair_q * 4)

    def _export_figure_tfm(self, save_path, line_pair):
        self.__zfile.zSetField(0, 3, 4, 0)
        self.__zfile.zSetField(1, 0, 0, 1)
        self.__zfile.zSetField(2, 0, 0.6 * self._imh, 1)
        self.__zfile.zSetField(3, 0, 0.8 * self._imh, 1)
        self.__zfile.zSetField(4, 0, self._imh, 1)
        self.__zfile.zModifySettings(
            save_path.joinpath("tmp.CFG"), "TFM_FREQ", line_pair
        )
        self.__zfile.zGetMetaFile(
            save_path.joinpath("tfm.wmf"), "Tfm", save_path.joinpath("tmp.CFG"), 1
        )
        self.__set_default_field()

    def _export_figure_tfm_default(self, save_path):
        self._export_figure_tfm(save_path, self._line_pair_q)

    def _export_figure_spt(self, save_path):
        self.__zfile.zGetMetaFile(save_path.joinpath("spt.wmf"), "Spt")

    def _export_figure_distortion_tan(self, save_path):
        self.__zfile.zGetMetaFile(
            save_path.joinpath("fcd_tan.wmf"),
            "Fcd",
            CONFIG_FOLDER.joinpath("distortion_tan.CFG"),
            1,
        )

    def _export_figure_distortion_ftheta(self, save_path):
        self.__zfile.zGetMetaFile(
            save_path.joinpath("fcd_ftheta.wmf"),
            "Fcd",
            CONFIG_FOLDER.joinpath("distortion_ftheta.CFG"),
            1,
        )

    def export_fig(self, fig_code):
        """Give the operand code in it and get the figure. The supported operand code are following:

        rel: Relative illumination
        mtf: mtf vs line pair
        tfm: through focus mtf
        fcd-tan: field curvature and distortion calculated by using tangent theta
        fcd-ftheta: field curvature and distortion calculated by using f theta

        """
        repo = find_optical_repo_path()
        fig_code = fig_code.lower()
        figs = {
            "rel": self._export_figure_ri,
            "mtf": self._export_figure_mtfvslp_default,
            "tfm": self._export_figure_tfm_default,
            "spt": self._export_figure_spt,
            "fcd-tan": self._export_figure_distortion_tan,
            "fcd-ftheta": self._export_figure_distortion_ftheta,
        }

        if fig_code not in figs:
            print(
                f"The operand code, {fig_code}, is not supported by"
                " ZDDEProjectionLensDataExtractor."
            )
        else:
            print(fig_code)
            figs.get(fig_code)(repo)


def log_data(file, refresh=False, engine="pyzdde"):
    repo = find_optical_repo_path()
    json_file = repo.joinpath(CONST["DATA"] + ".json")
    data = load_json_data(json_file)

    if refresh:
        extract_operand_code = data.keys()
    else:
        extract_operand_code = [
            operand_code for operand_code in data if data[operand_code] is None
        ]

    if engine == "pyzdde":
        with Zemax14(file) as zfile:
            data_extractor = ZDDEProjectionLensDataExtractor(zfile)
            for operand_code in extract_operand_code:
                data[operand_code] = data_extractor.extract(operand_code)
    elif engine == "zos-api":
        pass
    else:
        pass

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f)


def export_figs(file, engine="pyzdde"):
    repo = find_optical_repo_path()
    json_file = repo.joinpath(CONST["EXPORT-FIG"] + ".json")
    figs = load_json_data(json_file)

    export_operand_code = [fig for fig in figs.keys() if figs.get(fig)]

    if engine == "pyzdde":
        with Zemax14(file) as zfile:
            data_extractor = ZDDEProjectionLensDataExtractor(zfile)
            for fig_code in export_operand_code:
                data_extractor.export_fig(fig_code)
    elif engine == "zos-api":
        pass
    else:
        pass


if __name__ == "__main__":
    pass
