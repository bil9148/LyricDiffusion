import os
from tqdm import tqdm
from PySide6 import QtWidgets
import gui
import logging
import cv2


class Images2Video:
    def __init__(self, imagesPath, outputPath, outputFileName, uiWidget=None):
        self.imagesPath: str = imagesPath
        self.outputPath: str = outputPath
        self.outputFileName: str = outputFileName
        self.uiWidget = uiWidget

    def get_read_images(self):
        # Check if the images path exists
        if not os.path.exists(self.imagesPath):
            raise Exception("Images path does not exist.")

        images = []

        files = os.listdir(self.imagesPath)

        # Sort the files by name
        files.sort(key=lambda f: int(os.path.splitext(os.path.basename(f))[0]))

        # Check if there are any images in the images path
        for file in files:
            if file.endswith(".png"):

                # If size is < 1, skip the image
                read_img = cv2.imread(os.path.join(self.imagesPath, file))

                if read_img is None or read_img.size < 1:
                    continue

                images.append(read_img)

        return images

    def generate(self):
        try:
            """Generates a video from the images in the given path"""

            logging.info(
                f"Generating video from images in {self.imagesPath}...")

            # Create the output directory
            os.makedirs(self.outputPath, exist_ok=True)

            # Get all the images in the given path
            read_Images = self.get_read_images()

            if not read_Images or len(read_Images) == 0:
                raise Exception("No images found.")

            height, width, layers = read_Images[0].shape

            # Create the video writer with appropriate codec
            video = cv2.VideoWriter(
                os.path.join(self.outputPath, self.outputFileName), cv2.VideoWriter_fourcc(*'mp4v'), 12, (width, height))

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
                        self.uiWidget.textbox_info.setText(
                            f"Processing {read_img}")

                        # Force UI update
                        QtWidgets.QApplication.processEvents()

                except Exception as e:
                    gui.BasicUI.HandleError(e)

            video.release()

            if self.uiWidget is not None:
                self.uiWidget.loading_bar.setValue(
                    self.uiWidget.loading_bar.maximum())
                self.uiWidget.textbox_info.setText("Done")

        except Exception as e:
            gui.BasicUI.HandleError(e)
