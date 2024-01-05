# import images2Video
# import unittest
# import shutil
# import os


# class TestImages2Video(unittest.TestCase):
#     def setUp(self):
#         # Setup temp directory
#         self.temp_dir = os.path.join(os.getcwd(), "temp", "test", "images")
#         os.makedirs(self.temp_dir, exist_ok=True)

#     def tearDown(self):
#         # Delete temp directory recursively
#         shutil.rmtree(self.temp_dir)

#     def create_black_image(self, image_path):
#         # Create black image
#         with open(image_path, "w") as f:
#             f.write("")

#     def test_I2V_generate(self):
#         # Arrange
#         images = ["1.png", "2.png"]
#         output_path = os.path.join(self.temp_dir, "test", "videos")

#         # Create black images
#         for i in range(len(images)):
#             image_path = os.path.join(self.temp_dir, images[i])
#             self.create_black_image(image_path)

#         # Act
#         images2video = images2Video.Images2Video(
#             self.temp_dir, output_path, None)
#         images2video.generate()

#         # Check if output files were created
#         for i in range(len(images)):
#             file_path = os.path.join(output_path, f"{i}.mp4")
#             self.assertTrue(os.path.exists(file_path),
#                             f"File {file_path} not found.")
