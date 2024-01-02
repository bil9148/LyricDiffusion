import sys
from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
import lyrics2Images
import logging

class FontManager:
    @staticmethod
    def getFont() -> QtGui.QFont:
        return QtGui.QFont("Arial", 14)

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets and set common font
        self.label_outputPath = self.create_label("Output path:")
        self.textbox_outputPath = self.create_textbox()
        self.button_browseOutputPath = self.create_button("Browse")

        # Connect button signal
        self.button_browseOutputPath.clicked.connect(self.browseOutputPath)

        # Create layout and add widgets
        self.layout = QtWidgets.QGridLayout()   

        self.layout.addWidget(self.label_outputPath, 0, 0)

        self.layout.addWidget(self.textbox_outputPath, 0, 1)
        self.layout.addWidget(self.button_browseOutputPath, 0, 2)

        self.setLayout(self.layout)




class LyricsGeneratorWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets and set common font
        self.label_songName = self.create_label("Song name:")
        self.label_artistName = self.create_label("Artist name:")
        self.textbox_songName = self.create_textbox()
        self.textbox_artistName = self.create_textbox()
        self.label_modelList = self.create_label("Model:")
        self.label_numInferenceSteps = self.create_label(
            "Num inference steps:")
        self.textbox_numInferenceSteps = self.create_textbox()
        self.textbox_numInferenceSteps.setText("50")
        self.label_info = self.create_label("Info:")
        self.textbox_info = self.create_textbox(read_only=True)
        self.loading_bar = self.create_progress_bar()
        #Item list:
        # model_list.addItem("stabilityai/stable-diffusion-2-1")
        # model_list.addItem("DGSpitzer/Cyberpunk-Anime-Diffusion")
        # Generates black images
        # model_list.addItem("dataautogpt3/OpenDalleV1.1")
        # model_list.addItem("stabilityai/sdxl-turbo")
        # Don't work - no such modeling files are available
        # self.modelList.addItem("SG161222/Realistic_Vision_V2.0")
        # self.modelList.addItem("SG161222/Realistic_Vision_V6.0_B1_noVAE")
        # self.modelList.addItem("Lykon/DreamShaper")
        itemList = ["stabilityai/stable-diffusion-2-1", "DGSpitzer/Cyberpunk-Anime-Diffusion"]
        self.modelList = self.create_model_list(itemList=itemList)
        self.button_generate = self.create_button("Generate")

        # Connect button signal
        self.button_generate.clicked.connect(self.generate)

        # Create layout and add widgets
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.textbox_artistName, 0, 1)
        self.layout.addWidget(self.label_artistName, 0, 0)
        self.layout.addWidget(self.label_songName, 1, 0)
        self.layout.addWidget(self.textbox_songName, 1, 1)
        self.layout.addWidget(self.label_modelList, 2, 0)
        self.layout.addWidget(self.modelList, 2, 1)
        self.layout.addWidget(self.label_numInferenceSteps, 3, 0)
        self.layout.addWidget(self.textbox_numInferenceSteps, 3, 1)
        self.layout.addWidget(self.label_info, 4, 0)
        self.layout.addWidget(self.textbox_info, 4, 1)
        self.layout.addWidget(self.loading_bar, 5, 0, 1, -1)
        self.layout.addWidget(self.button_generate, 6, 0, 1, -1)

        self.setLayout(self.layout)    

    def create_label(self, text):
        label = QtWidgets.QLabel(text)
        label.setFont(FontManager.getFont())
        return label

    def create_textbox(self, read_only=False):
        textbox = QtWidgets.QLineEdit()
        textbox.setFont(FontManager.getFont())
        textbox.setReadOnly(read_only)
        return textbox

    def create_progress_bar(self):
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setFont(FontManager.getFont())
        progress_bar.setMinimum(0)
        progress_bar.setValue(0)
        progress_bar.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return progress_bar

    def create_model_list(self, itemList: Optional[list] = None):
        model_list = QtWidgets.QComboBox()

        if itemList is not None:
            model_list.addItems(itemList)

        model_list.setFont(FontManager.getFont())
        return model_list

    def create_button(self, text):
        button = QtWidgets.QPushButton(text)
        button.setFont(FontManager.getFont())
        return button

    def generate(self):
        try:                
            songName = self.textbox_songName.text()
            artistName = self.textbox_artistName.text()

            model_id = self.modelList.currentText()

            assert self.textbox_numInferenceSteps.text(
            ) and self.textbox_numInferenceSteps.text().isnumeric(), "Number of inference steps must be a number"

            num_inference_steps = int(self.textbox_numInferenceSteps.text())

            # Validate the input
            assert songName and len(songName) > 0, "Song name cannot be empty"
            assert artistName and len(
                artistName) > 0, "Artist name cannot be empty"
            assert  num_inference_steps > 0 and num_inference_steps <= 100, "Number of inference steps must be between 1 and 100"

            lyrics2Images.run(song_name=songName, artist_name=artistName,
                            model_id=model_id, num_inference_steps=num_inference_steps, uiWidget=self)
        except Exception as e:
            message = e.args[0] if len(e.args) > 0 else str(e)
            self.HandleError(message)
            self.loading_bar.setValue(0)

    def HandleError(self, message, silent=False):
        logging.error(message)
        
        if not silent:
            self.MsgBox(message)

    def MsgBox(self, e):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(str(e))
        msg.setWindowTitle("Lyrics2Images")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)            
        msg.exec_()

class LyricsGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = LyricsGeneratorWidget()
        self.setCentralWidget(self.central_widget)

        self.resize(600, 400)
        self.setWindowTitle("Lyrics2Images")


def showGUI():
    app = QtWidgets.QApplication([])

    main_app = LyricsGeneratorApp()
    main_app.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    showGUI()
