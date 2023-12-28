from ..lyrics2Images import Lyrics2Images
import unittest
import tempfile
import shutil
import os


class TestLyrics2Images(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_runL2I_with_valid_verses(self):
        # Arrange
        verses = ["Verse 1", "Verse 2", "Verse 3"]
        output_path = os.path.join(self.temp_dir, "output")

        # Act
        lyrics2images = Lyrics2Images(use_auth_token=False)
        lyrics2images.generate(verses, output_path)

        # Check if output files were created
        for i in range(len(verses)):
            file_path = os.path.join(output_path, f"{i}.png")
            self.assertTrue(os.path.exists(file_path),
                            f"File {file_path} not found.")


if __name__ == '__main__':
    unittest.main()
