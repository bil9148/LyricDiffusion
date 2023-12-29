from ..lyrics2Images import Lyrics2Images
import unittest
import shutil
import os
from output import OUTPUT_PATH


class TestLyrics2Images(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(OUTPUT_PATH, "images", "test")
        os.makedirs(self.temp_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_runL2I_with_valid_verses(self):
        # Arrange
        verses = ["Verse 1", "Verse 2"]
        output_path = os.path.join(
            OUTPUT_PATH, "images", "test")

        # Act
        lyrics2images = Lyrics2Images(use_auth_token=False)
        lyrics2images.generate(verses, output_path, None)

        # Check if output files were created
        for i in range(len(verses)):
            file_path = os.path.join(output_path, f"{i}.png")
            self.assertTrue(os.path.exists(file_path),
                            f"File {file_path} not found.")


if __name__ == '__main__':
    unittest.main()
