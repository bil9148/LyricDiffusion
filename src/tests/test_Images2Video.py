import images2Video
import unittest
import shutil
import os


# class TestImages2Video(unittest.TestCase):
#     def setUp(self):
#         # Setup temp directory
#         self.temp_dir = os.path.join(os.getcwd(), "temp")

#     def tearDown(self):
#         # Delete temp directory recursively
#         shutil.rmtree(self.temp_dir)

#     def test_runI2V_with_valid_images(self):
#         # Arrange
#         images = ["test_images/1.png", "test_images/2.png"]
#         output_path = os.path.join(self.temp_dir, "test", "videos")

#         # Act
#         images2video = images2Video.Images2Video()
#         images2video.generate(images, output_path, None)

#         # Check if output files were created
#         for i in range(len(images)):
#             file_path = os.path.join(output_path, f"{i}.mp4")
#             self.assertTrue(os.path.exists(file_path),
#                             f"File {file_path} not found.")
