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

class BasicUI:
    @staticmethod
    def HandleError(message, silent=False):
        logging.error(message)
        
        if not silent:
            MsgBox(message)

    @staticmethod
    def MsgBox(e):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(str(e))
        msg.setWindowTitle("Lyrics2Images")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)            
        msg.exec_()

    @staticmethod
    def create_label(text):
        label = QtWidgets.QLabel(text)
        label.setFont(FontManager.getFont())
        return label

    @staticmethod
    def create_textbox(read_only=False):
        textbox = QtWidgets.QLineEdit()
        textbox.setFont(FontManager.getFont())
        textbox.setReadOnly(read_only)
        return textbox

    @staticmethod
    def create_progress_bar():
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setFont(FontManager.getFont())
        progress_bar.setMinimum(0)
        progress_bar.setValue(0)
        progress_bar.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return progress_bar

    @staticmethod
    def create_model_list( itemList: Optional[list] = None):
        model_list = QtWidgets.QComboBox()

        if itemList is not None:
            model_list.addItems(itemList)

        model_list.setFont(FontManager.getFont())
        return model_list

    @staticmethod
    def create_button( text):
        button = QtWidgets.QPushButton(text)
        button.setFont(FontManager.getFont())
        return button

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets and set common font
        self.label_outputPath = BasicUI.create_label("Output path:")
        self.textbox_outputPath = BasicUI.create_textbox()
        self.button_browseOutputPath = BasicUI.create_button("Browse")

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
        self.label_songName = BasicUI.create_label("Song name:")
        self.label_artistName = BasicUI.create_label("Artist name:")
        self.textbox_songName = BasicUI.create_textbox()
        self.textbox_artistName = BasicUI.create_textbox()
        self.label_modelList = BasicUI.create_label("Model:")
        self.label_numInferenceSteps = BasicUI.create_label(
            "Num inference steps:")
        self.textbox_numInferenceSteps = BasicUI.create_textbox()
        self.textbox_numInferenceSteps.setText("50")
        self.label_info = BasicUI.create_label("Info:")
        self.textbox_info = BasicUI.create_textbox(read_only=True)
        self.loading_bar = BasicUI.create_progress_bar()        
        # Generate black images
        # model_list.addItem("dataautogpt3/OpenDalleV1.1")
        # model_list.addItem("stabilityai/sdxl-turbo")
        # Don't work - no such modeling files are available
        # self.modelList.addItem("SG161222/Realistic_Vision_V2.0")
        # self.modelList.addItem("SG161222/Realistic_Vision_V6.0_B1_noVAE")
        # self.modelList.addItem("Lykon/DreamShaper")
        itemList = ["stabilityai/stable-diffusion-2-1", "DGSpitzer/Cyberpunk-Anime-Diffusion"]
        self.modelList = BasicUI.create_model_list(itemList=itemList)
        self.button_generate = BasicUI.create_button("Generate")
        self.button_settings = BasicUI.create_button("Settings")

        # Connect button signal
        self.button_generate.clicked.connect(self.generate)
        self.button_settings.clicked.connect(self.showSettings)

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
        self.layout.addWidget(self.button_generate, 6, 1) 
        self.layout.addWidget(self.button_settings, 6, 0) 


        self.setLayout(self.layout)    

    def showSettings(self):
        pass

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
            BasicUI.HandleError(message)
            self.loading_bar.setValue(0)#

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
