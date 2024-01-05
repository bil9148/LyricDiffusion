import images2Video
import unittest
import shutil
import os
from PIL import Image, ImageDraw


class TestImages2Video(unittest.TestCase):
    def setUp(self):
        # Setup temp directory
        self.temp_dir = os.path.join(os.getcwd(), "temp", "test")
        self.images_dir = os.path.join(self.temp_dir, "images")
        self.videos_dir = os.path.join(self.temp_dir, "videos")
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.videos_dir, exist_ok=True)

    def tearDown(self):
        # Delete temp directory recursively
        # shutil.rmtree(self.temp_dir)
        pass

    def generate_non_empty_image(file_path):
        # Create a new image with a white background
        width, height = 200, 200  # Adjust the dimensions as needed
        image = Image.new("RGB", (width, height), "white")

        # Draw a rectangle on the image (for illustration purposes)
        draw = ImageDraw.Draw(image)
        # Adjust the rectangle coordinates
        rectangle_coords = [(50, 50), (150, 150)]
        draw.rectangle(rectangle_coords, fill="blue")

        # Save the image to the specified file path
        image.save(file_path)

    def test_I2V_generate(self):
        # Arrange
        images = ["1.png", "2.png"]

        # Generate sample image
        for image in images:
            file_path = os.path.join(self.images_dir, image)
            TestImages2Video.generate_non_empty_image(file_path)

        # Act
        images2video = images2Video.Images2Video(
            self.images_dir, self.videos_dir, "video.mp4")
        images2video.generate()

        outputFileName = os.path.join(self.videos_dir, "video.mp4")

        # Check if output file was created
        self.assertTrue(os.path.exists(outputFileName),
                        f"File {outputFileName} not found.")
