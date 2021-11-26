from unittest.case import TestCase
import unittest
import json
from pprint import pprint
from io import StringIO
from .common import find_optical_repo_path
from .common import load_json_data


def create_lens_template(template):
    repo = find_optical_repo_path()
    test_criterion_file = repo.joinpath("criterion.json")
    with open(test_criterion_file, 'w', encoding="utf-8") as jfile:
        json.dump(template, jfile)


def exc_lens_test():
    repo = find_optical_repo_path()
    data_file = repo.joinpath("data.json")
    test_criterion_file = repo.joinpath("criterion.json")
    lens_data = load_json_data(data_file)
    test_criterion = load_json_data(test_criterion_file)
    skip_msg = "You did not extract the data or set the criterion"

    class ProjectionLensTestCase(TestCase):
        @unittest.skipIf(
            lens_data['op-ttl'] is None or test_criterion["op-ttl"] is None, skip_msg
        )
        def test_op_ttl(self):
            ttl = lens_data['op-ttl']
            expected = float(test_criterion['op-ttl'])
            self.assertLessEqual(ttl, expected)

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
