import unittest
from unittest.mock import patch
import logging
from settings import OutputPath, SkipEmptyVerses, Logger


class TestOutputPath(unittest.TestCase):

    def test_get_default_output_path(self):
        default_output_path = OutputPath.getDefaultOutputPath()
        self.assertIsInstance(default_output_path, str)

    def test_set_output_path(self):
        with patch('logging.info') as mock_logging_info:
            OutputPath.setOutputPath("/path/to/output")
            mock_logging_info.assert_called_with(
                "Output path updated to /path/to/output.")

    def test_get_output_path(self):
        expected_output_path = "/path/to/output"
        OutputPath.setOutputPath(expected_output_path)
        output_path = OutputPath.getOutputPath()
        self.assertEqual(output_path, expected_output_path,
                         f"output_path: {output_path}, expected: {expected_output_path}")


class TestSkipEmptyVerses(unittest.TestCase):

    def test_set_skip_empty_verses(self):
        with patch('logging.info') as mock_logging_info:
            SkipEmptyVerses.setSkipEmptyVerses(True)
            mock_logging_info.assert_called_with(
                "Skip empty verses updated to True.")

    def test_get_skip_empty_verses_true(self):
        expected_skip_empty_verses = True
        SkipEmptyVerses.setSkipEmptyVerses(expected_skip_empty_verses)
        result = SkipEmptyVerses.getSkipEmptyVerses()
        self.assertEqual(result, expected_skip_empty_verses,
                         f"result: {result}, expected: {expected_skip_empty_verses}")

    def test_get_skip_empty_verses_false(self):
        expected_skip_empty_verses = False
        SkipEmptyVerses.setSkipEmptyVerses(expected_skip_empty_verses)
        result = SkipEmptyVerses.getSkipEmptyVerses()
        self.assertEqual(result, expected_skip_empty_verses,
                         f"result: {result}, expected: {expected_skip_empty_verses}")


class TestLogger(unittest.TestCase):

    def test_get_log_file_path(self):
        log_file_path = Logger.getLogFilePath()
        self.assertIsInstance(log_file_path, str)


if __name__ == '__main__':
    unittest.main()
