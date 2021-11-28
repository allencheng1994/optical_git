from unittest.case import TestCase
import unittest
import json
from pprint import pprint
from io import StringIO
from .common import find_optical_repo_path
from .common import load_json_data
from .config import CONST


def exc_projection_lens_test():
    repo = find_optical_repo_path()
    data_file = repo.joinpath(CONST["DATA"] + ".json")
    test_criterion_file = repo.joinpath(CONST["CRITERION"] + ".json")
    spec_target_file = repo.joinpath(CONST["SPEC_TARGET"] + ".json")
    lens_data = load_json_data(data_file)
    spec_data = load_json_data(spec_target_file)
    test_criterion = load_json_data(test_criterion_file)
    skip_msg = "You did not extract the data or set the criterion"

    class ProjectionLensTestCase(TestCase):
        @unittest.skipIf(
            lens_data.get('op-ttl') is None or spec_data.get("op-ttl") is None, skip_msg
        )
        def test_op_ttl(self):
            ttl = lens_data['op-ttl']
            expected = test_criterion['op-ttl']
            self.assertLessEqual(ttl, expected)

        @unittest.skipIf(
            lens_data.get('op-dfov') is None or spec_data.get("op-dfov") is None,
            skip_msg,
        )
        def test_op_dfov(self):
            dfov = lens_data['op-dfov']
            expected = spec_data['op-dfov']
            criterion = test_criterion['op-dfov']
            msg = f'The op-dfov {dfov} is not in the criterion {criterion}'
            self.assertAlmostEqual(dfov, expected, msg=msg, delta=criterion)

        @unittest.skipIf(
            lens_data.get('ri') is None or spec_data.get('ri') is None, skip_msg
        )
        def test_ri(self):
            ri = lens_data['ri']
            expected = spec_data['ri']
            self.assertGreaterEqual(ri, expected)

        @unittest.skipIf(lens_data.get('wfno') is None, skip_msg)
        def test_fcgs(self):
            wfno = lens_data['wfno']
            expected = spec_data['fno']
            criterion = test_criterion['wfno']
            wfno_percentage = abs((wfno - expected) / expected)
            self.assertLessEqual(wfno_percentage, criterion)

        @unittest.skipIf(lens_data.get('fcgs') is None, skip_msg)
        def test_fcgs(self):
            fcgs = lens_data['fcgs']
            expected = 0
            criterion = test_criterion['fcgs']
            msg = f'The fcgs {fcgs} is not in the criterion {criterion}'
            self.assertAlmostEqual(fcgs, expected, msg=msg, delta=criterion)

        @unittest.skipIf(
            lens_data.get('cra') is None or spec_data['cra'] is None, skip_msg
        )
        def test_cra(self):
            cra = lens_data['cra']
            expected_cra = spec_data['cra']
            criterion_lower = test_criterion['cra-lower']
            criterion_upper = test_criterion['cra-upper']
            for lens_cra, sensor_cra in zip(cra, expected_cra):
                with self.subTest(
                    msg="lens cra testing", lens_cra=lens_cra, sensor_cra=sensor_cra
                ):
                    err_msg = (
                        f'The cra {lens_cra} is lower than the criterion'
                        f' {sensor_cra + criterion_lower} or larger than the criterion'
                        f' {sensor_cra + criterion_upper}'
                    )
                    difference = lens_cra - sensor_cra
                    self.assertTrue(
                        difference <= criterion_upper or difference >= criterion_lower,
                        msg=err_msg,
                    )

    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(unittest.makeSuite(ProjectionLensTestCase))
    print(f"Test run {result.testsRun}")
    print(f"Errors {result.errors}")
    pprint(result.failures)
    stream.seek(0)
    print(f"Test ouput\n {stream.read()}")


if __name__ == '__main__':
    pass
