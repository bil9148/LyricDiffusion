import os
from tqdm import tqdm
from PySide6 import QtWidgets
import gui
import logging
import cv2


class Images2Video:
    def __init__(self, imagesPath, outputPath, outputFileName, fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=12, uiWidget=None):
        self.imagesPath: str = imagesPath
        self.outputPath: str = outputPath
        self.outputFileName: str = outputFileName
        self.uiWidget = uiWidget
        self.fps: int = int(fps)
        self.fourcc = fourcc

    @staticmethod
    def get_fourcc_for(formatName):
        # The 2 most common video formats
        formats = {
            "mp4": cv2.VideoWriter_fourcc(*'mp4v'),
            "avi": cv2.VideoWriter_fourcc(*'DIVX')
        }

        return formats.get(formatName, formats["mp4"])

    def get_read_images(self):
        # Check if the images path exists
        if not os.path.exists(self.imagesPath):
            raise Exception("Images path does not exist.")

        images = []

        files = os.listdir(self.imagesPath)

        # Check if there are any images in the images path
        for file in files:
            if file.endswith(".png"):

                # If size is < 1, skip the image
                read_img = cv2.imread(os.path.join(self.imagesPath, file))

                if read_img is None or read_img.size < 1:
                    continue

                images.append((file, read_img))

        if len(images) == 0:
            raise Exception("No images found.")

        # Sort the images by file name
        images.sort(key=lambda x: int(
            os.path.splitext(os.path.basename(x[0]))[0]))

        # Extract the sorted images without file names
        sorted_images = [image[1] for image in images]

        return sorted_images

    def generate(self):
        try:
            """Generates a video from the images in the given path"""

            # Get all the images in the given path
            read_Images = self.get_read_images()

            if not read_Images or len(read_Images) == 0:
                raise Exception("No images found.")

            height, width, layers = read_Images[0].shape

            # Create the output directory
            os.makedirs(self.outputPath, exist_ok=True)

            logging.info(
                f"Starting video generation at {self.outputPath}.\nVideo name: {self.outputFileName}.\nVideo FPS: {self.fps}.\nVideo codec: {self.fourcc}")

            # Create the video writer with appropriate codec
            video = cv2.VideoWriter(
                os.path.join(self.outputPath, self.outputFileName), self.fourcc, self.fps, (width, height))

            if self.uiWidget is not None:
                self.uiWidget.loading_bar.setMaximum(len(read_Images))
                self.uiWidget.loading_bar.setValue(0)

            # Add each image to the video using imageio
            for read_img in read_Images:
                try:
                    # Write to the video
                    video.write(read_img)

                    # Update the UI
                    if self.uiWidget is not None:
                        self.uiWidget.loading_bar.setValue(
                            self.uiWidget.loading_bar.value() + 1)

                        # Force UI update
                        QtWidgets.QApplication.processEvents()

                except Exception as e:
                    gui.BasicUI.HandleError(e)

            video.release()

            if self.uiWidget is not None:
                self.uiWidget.loading_bar.setValue(
                    self.uiWidget.loading_bar.maximum())

        except Exception as e:
            gui.BasicUI.HandleError(e)
