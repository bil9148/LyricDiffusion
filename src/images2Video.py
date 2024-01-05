import os
import cv2
from tqdm import tqdm
from PyQt5 import QtWidgets
import gui


class Images2Video:
    def __init__(self, imagesPath, outputPath, outputFileName, uiWidget=None):
        self.imagesPath: str = imagesPath
        self.outputPath: str = outputPath
        self.outputFileName: str = outputFileName
        self.uiWidget = uiWidget

    def get_images(self):
        # Check if the images path exists
        if not os.path.exists(self.imagesPath):
            raise Exception("Images path does not exist.")

        images = []

        # Check if there are any images in the images path
        for file in os.listdir(self.imagesPath):
            if file.endswith(".png"):
                images.append(os.path.join(self.imagesPath, file))

        if not images or len(images) == 0:
            raise Exception("No images found.")

        # Sort the images by name
        images.sort(key=lambda f: int(
            os.path.splitext(os.path.basename(f))[0]))

        return images

    def generate(self):
        try:
            """Generates a video from the images in the given path"""
            # Create the output directory
            os.makedirs(self.outputPath, exist_ok=True)

            # Get all the images in the given path
            images = self.get_images()

            # Find the first valid image
            while images and os.path.getsize(images[0]) < 100:
                images.pop(0)

            if not images or os.path.getsize(images[0]) < 100:
                raise Exception("No valid images found.")

            # Get the image size
            img = cv2.imread(images[0])

            if img is None:
                raise Exception("Could not read the image.")

            height, width, layers = img.shape

            # Create the video writer
            video = cv2.VideoWriter(os.path.join(
                self.outputPath, self.outputFileName), 0, 1, (width, height))

            if self.uiWidget is not None:
                self.uiWidget.loading_bar.setMaximum(len(images))
                self.uiWidget.loading_bar.setValue(0)

            # Add each image to the video
            for image in tqdm(images):
                video.write(cv2.imread(image))
                print(image)
                # Update the UI
                if self.uiWidget is not None:
                    self.uiWidget.textbox_info.setText(f"Processing {image}")

                    # Force UI update
                    QtWidgets.QApplication.processEvents()

            # Release the video writer
            video.release()

            if self.uiWidget is not None:
                self.uiWidget.loading_bar.setValue(
                    self.uiWidget.loading_bar.maximum())
                self.uiWidget.textbox_info.setText("Done")
        except Exception as e:
            gui.BasicUI.HandleError(e)
