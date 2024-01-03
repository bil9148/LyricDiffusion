import unittest
import utils


class TestUtils(unittest.TestCase):
    def test_get_all_models(self):
        models = utils.HuggingFace().get_all_model_names(
            limit=5, direction=-1, sort="downloads")

        self.assertIsNotNone(models, "Models should not be None")
        self.assertEqual(len(models), 5, "Lengtt of Models should be 5")
