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
            self.assertAlmostEqual(dfov, expected, messgae=msg, delta=criterion)

        @unittest.skipIf(
            lens_data.get('ri') is None or spec_data.get('ri') is None, skip_msg
        )
        def test_ri(self):
            ri = lens_data['ri']
            expected = spec_data['ri']
            self.assertGreaterEqual(ri, expected)

        @unittest.skipIf(lens_data.get('fcgs') is None, skip_msg)
        def test_fcgs(self):
            fcgs = lens_data['fcgs']
            expected = 0
            criterion = test_criterion['fcgs']
            msg = f'The op-dfov {dfov} is not in the criterion {criterion}'
            self.assertAlmostEqual(fcgs, expected, messgae=msg, delta=criterion)

        @unittest.skipIf(lens_data.get('cra') is None, skip_msg)
        def test_cra0(self):
            cra = lens_data['cra'][0]
            expected = spec_data['cra0']
            criterion = test_criterion['fcgs']
            msg = f'The op-dfov {dfov} is not in the criterion {criterion}'
            self.assertAlmostEqual(fcgs, expected, messgae=msg, delta=criterion)

    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(unittest.makeSuite(ProjectionLensTestCase))
    print(f"Tess run {result.testsRun}")
    print(f"Errors {result.errors}")
    pprint(result.failures)
    stream.seek(0)
    print(f"Test ouput\n {stream.read()}")


if __name__ == '__main__':
    pass
