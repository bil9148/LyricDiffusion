import os
import cv2
from tqdm import tqdm
from PyQt5 import QtWidgets
import gui


class Images2Video:
    def __init__(self, imagesPath, outputPath, uiWidget):
        self.imagesPath = imagesPath
        self.outputPath = outputPath
        self.uiWidget = uiWidget

    def generate(self):
        """Generates a video from the images in the given path"""
        # TODO: Finish this
        pass

        try:
            """Generates a video from the images in the given path"""
            # Create the output directory
            os.makedirs(self.outputPath, exist_ok=True)

            # Get the list of images
            images = [os.path.join(self.imagesPath, f)
                      for f in os.listdir(self.imagesPath) if f.endswith(".png")]

            if images is None or len(images) == 0:
                raise Exception("No images found.")

            # Sort the images by name
            images.sort(key=lambda f: int(
                os.path.splitext(os.path.basename(f))[0]))

            # Get the first image
            image = images[0]

            # Get the image size
            img = cv2.imread(image)
            height, width, layers = img.shape

            # Create the video writer
            video = cv2.VideoWriter(os.path.join(
                self.outputPath, "video.mp4"), 0, 1, (width, height))

            if self.uiWidget is not None:
                self.uiWidget.loading_bar.setMaximum(len(images))
                self.uiWidget.loading_bar.setValue(0)

            # Add each image to the video
            for image in tqdm(images):
                video.write(cv2.imread(image))

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
