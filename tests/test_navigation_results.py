"""Reject incomplete Unity navigation evidence; real input execution is a separate gate."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("navigation_runner", ROOT / "tools/run_navigation_fixture.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class NavigationResultsTests(unittest.TestCase):
    def validate(self, names=None, result="Passed", case_result="Passed"):
        root = ET.Element("test-run", result=result)
        for name in sorted(runner.EXPECTED_TESTS if names is None else names):
            ET.SubElement(root, "test-case", name=name, result=case_result)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "results.xml"
            ET.ElementTree(root).write(path)
            return runner.validate_results(path)

    def test_complete_pass(self):
        self.assertEqual(len(runner.EXPECTED_TESTS), self.validate())

    def test_missing_mutation_probe_fails(self):
        with self.assertRaises(RuntimeError):
            self.validate(runner.EXPECTED_TESTS - {"DuplicateRouterMutationIsDetected"})

    def test_no_tests_fails(self):
        with self.assertRaises(RuntimeError):
            self.validate(set())

    def test_failed_or_skipped_case_fails_even_with_passing_envelope(self):
        for result in ("Failed", "Skipped", "Inconclusive"):
            with self.subTest(result=result), self.assertRaises(RuntimeError):
                self.validate(case_result=result)

    def test_failed_envelope_fails(self):
        with self.assertRaises(RuntimeError):
            self.validate(result="Failed(Child)")

    def test_duplicate_case_fails(self):
        with self.assertRaises(RuntimeError):
            self.validate(list(runner.EXPECTED_TESTS) + [next(iter(runner.EXPECTED_TESTS))])
