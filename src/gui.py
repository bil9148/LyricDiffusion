import sys
from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QTabWidget
import lyrics2Images
import images2Video
import settings as settings
import utils
import os


class FontManager:
    @staticmethod
    def getFont() -> QtGui.QFont:
        return QtGui.QFont("Arial", 12)


class BasicUI:
    @staticmethod
    def HandleError(exception: Exception, silent=False):
        settings.logging.error(exception, exc_info=True)

        # If not silent and UI is available, show error message
        if not silent and QtWidgets.QApplication.instance():
            BasicUI.MsgBox(exception)

    @staticmethod
    def AskYesNo(text):
        if not QtWidgets.QApplication.instance():
            return True

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText(text)
        msg.setWindowTitle("Lyrics2Images")
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        return msg.exec_() == QtWidgets.QMessageBox.Yes

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
    def create_checkbox(text, checked=True):
        checkbox = QtWidgets.QCheckBox(text)
        checkbox.setChecked(checked)
        checkbox.setFont(FontManager.getFont())
        return checkbox

    @staticmethod
    def create_searchable_combobox(itemList: Optional[list] = None):
        combobox = QtWidgets.QComboBox()
        combobox.setEditable(True)
        combobox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        combobox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

        if itemList is not None:
            combobox.addItems(itemList)

        combobox.setFont(FontManager.getFont())

        return combobox

    @staticmethod
    def create_textbox(read_only=False, text="", placeholder_text=""):
        textbox = QtWidgets.QLineEdit()
        textbox.setFont(FontManager.getFont())
        textbox.setText(text)
        textbox.setPlaceholderText(placeholder_text)
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
    def create_combo_box(itemList: Optional[list] = None):
        model_list = QtWidgets.QComboBox()

        if itemList is not None:
            model_list.addItems(itemList)

        model_list.setFont(FontManager.getFont())
        return model_list

    @staticmethod
    def create_button(text):
        button = QtWidgets.QPushButton(text)
        button.setFont(FontManager.getFont())
        return button


class Lyrics2ImagesTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets and set common font
        self.label_songName = BasicUI.create_label("Song name:")
        self.label_artistName = BasicUI.create_label("Artist name:")
        self.textbox_songName = BasicUI.create_textbox(
            placeholder_text="e.g. Gangsta's Paradise")
        self.textbox_artistName = BasicUI.create_textbox(
            placeholder_text="e.g. Coolio")
        self.label_modelList = BasicUI.create_label("Model:")
        self.label_numInferenceSteps = BasicUI.create_label(
            "Num. inference steps:")
        self.textbox_numInferenceSteps = BasicUI.create_textbox(text="20")
        self.label_extra_prompt = BasicUI.create_label("Extra prompt:")
        self.textbox_extra_prompt = BasicUI.create_textbox(
            placeholder_text="e.g. dark ambiance, best quality, extremely detailed, epic")
        self.label_info = BasicUI.create_label("Info:")
        self.textbox_info = BasicUI.create_textbox(read_only=True)
        self.loading_bar = BasicUI.create_progress_bar()

        itemList = utils.HuggingFace.get_all_model_names(
            limit=30, direction=-1, sort="downloads")
        if itemList is None or len(itemList) < 1:
            itemList = ["stabilityai/stable-diffusion-2-1", "stabilityai/sdxl-turbo", "Lykon/dreamshaper-xl-turbo",
                        "DGSpitzer/Cyberpunk-Anime-Diffusion", "SG161222/Realistic_Vision_V2.0", "stabilityai/sd-turbo",
                        "SG161222/Realistic_Vision_V6.0_B1_noVAE", "Lykon/DreamShaper", "dataautogpt3/OpenDalleV1.1",]
        # Sort the list alphabetically
        itemList.sort()
        # self.modelList = BasicUI.create_combo_box(itemList=itemList)
        self.modelList = BasicUI.create_searchable_combobox(itemList=itemList)

        self.button_generate_images = BasicUI.create_button("Generate images")
        self.button_settings = BasicUI.create_button("Settings")

        # Connect button signals
        self.button_generate_images.clicked.connect(self.run_L2I)
        self.button_settings.clicked.connect(self.showSettings)

        self.setupLayout()

        self.setLayout(self.layout)

    def setupLayout(self):
        # Create layout and add widgets
        self.layout = QtWidgets.QGridLayout()

        self.layout.addWidget(self.textbox_artistName, 0, 1)
        self.layout.addWidget(self.label_artistName, 0, 0)
        self.layout.addWidget(self.label_songName, 1, 0)
        self.layout.addWidget(self.textbox_songName, 1, 1)
        self.layout.addWidget(self.label_modelList, 2, 0)
        self.layout.addWidget(self.modelList, 2, 1)
        self.layout.addWidget(self.label_numInferenceSteps, 3, 0)
        self.layout.addWidget(
            self.textbox_numInferenceSteps, 3, 1)
        self.layout.addWidget(self.label_extra_prompt, 4, 0)
        self.layout.addWidget(self.textbox_extra_prompt, 4, 1)
        self.layout.addWidget(self.label_info, 5, 0)
        self.layout.addWidget(self.textbox_info, 5, 1)
        self.layout.addWidget(self.loading_bar, 6, 0, 1, -1)
        self.layout.addWidget(self.button_generate_images, 7, 1)
        self.layout.addWidget(self.button_settings, 7, 0)

    def showSettings(self):
        self.settingsWidget = SettingsWidget()
        self.settingsWidget.show()

        self.settingsWidget.resize(600, 100)
        self.settingsWidget.setWindowTitle("Settings")

    def run_L2I(self):
        try:
            songName = self.textbox_songName.text()
            artistName = self.textbox_artistName.text()

            model_id = self.modelList.currentText()

            if not self.textbox_numInferenceSteps.text(
            ) or not self.textbox_numInferenceSteps.text().isnumeric():
                raise Exception("Number of inference steps cannot be empty")

            # Validate the input
            if not songName or len(songName) < 1:
                raise Exception("Song name cannot be empty")

            if not artistName or len(artistName) < 1:
                raise Exception("Artist name cannot be empty")

            if not model_id or len(model_id) < 1:
                raise Exception("Model ID cannot be empty")

            num_inference_steps = int(self.textbox_numInferenceSteps.text())

            if not num_inference_steps or num_inference_steps < 1 or num_inference_steps > 100:
                raise Exception(
                    "Number of inference steps must be between 1 and 100")

            lyrics2Images.Lyrics2Images.run(song_name=songName, artist_name=artistName, prompt=self.textbox_extra_prompt.text(),
                                            model_id=model_id, num_inference_steps=num_inference_steps, uiWidget=self)
        except Exception as e:
            BasicUI.HandleError(e)
            self.loading_bar.setValue(0)


class ImagesToVideoTab(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Create widgets and set common font
        self.label_images_path = BasicUI.create_label("Images path:")

        self.label_video_speed = BasicUI.create_label("Video speed:")
        self.textbox_video_speed = BasicUI.create_textbox(
            placeholder_text="(between 1 and 60) (default: 12)")

        self.textbox_images_path = BasicUI.create_textbox(
            read_only=True, placeholder_text="e.g. C:/Users/JohnDoe/Desktop/images")

        self.button_browse_images_path = BasicUI.create_button("Browse")

        self.loading_bar = BasicUI.create_progress_bar()

        self.button_generate_video = BasicUI.create_button("Generate video")

        # Connect button signals
        self.button_generate_video.clicked.connect(self.run_I2V)
        self.button_browse_images_path.clicked.connect(self.browseImagesPath)

        self.setupLayout()

        self.setLayout(self.layout)

    def setupLayout(self):
        # Create layout and add widgets
        self.layout = QtWidgets.QGridLayout()

        self.layout.addWidget(self.label_images_path, 0, 0)
        self.layout.addWidget(self.textbox_images_path, 0, 1)
        self.layout.addWidget(self.button_browse_images_path, 0, 2)

        self.layout.addWidget(self.label_video_speed, 1, 0)
        self.layout.addWidget(self.textbox_video_speed, 1, 1)

        self.layout.addWidget(self.loading_bar, 2, 0, 1, -1)
        self.layout.addWidget(self.button_generate_video, 3, 1)

    def browseImagesPath(self):
        temp = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select images path")

        if temp:
            self.textbox_images_path.setText(temp)

    def run_I2V(self):
        try:
            imagesPath = self.textbox_images_path.text()

            # Validate the input

            if not imagesPath or len(imagesPath) < 1:
                raise Exception("Images path cannot be empty")

            folderName = os.path.basename(
                os.path.normpath(imagesPath)).rstrip()
            # outputFileName should be the same as the last folder in imagesPath
            outputFileName = f"{folderName}.mp4"

            outputPath = os.path.join(
                settings.OutputPath.getOutputPath(), "videos")

            if not self.textbox_video_speed.text():
                raise Exception("Video speed cannot be empty")

            fps: int = self.textbox_video_speed.text()

            if not fps or not fps.isnumeric() or int(fps) < 1 or int(fps) > 60:
                raise Exception(
                    "Video speed must be a number between 1 and 60")

            i2v = images2Video.Images2Video(
                imagesPath=imagesPath, outputPath=outputPath, outputFileName=outputFileName, fps=fps, uiWidget=self)

            i2v.generate()

        except Exception as e:
            BasicUI.HandleError(e)
            self.loading_bar.setValue(0)


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(Lyrics2ImagesTab(), "Lyrics2Images")
        self.tabWidget.addTab(ImagesToVideoTab(), "Images2Video")

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.tabWidget)
        self.setLayout(self.layout)


class LyricsGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = MainWidget()
        self.setCentralWidget(self.central_widget)

        self.resize(700, 350)
        self.setWindowTitle("Lyrics2Images")


class SettingsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets and set common font
        self.label_outputPath = BasicUI.create_label("Output path:")
        self.textbox_outputPath = BasicUI.create_textbox(
            read_only=True, text=settings.OutputPath.getOutputPath())
        self.button_browseOutputPath = BasicUI.create_button("Browse")

        self.checkbox_skipEmptyVerses = BasicUI.create_checkbox(
            "Skip empty verses", settings.SkipEmptyVerses.getSkipEmptyVerses())

        # Connect checkbox signal
        self.checkbox_skipEmptyVerses.stateChanged.connect(
            self.skipEmptyVersesChanged)

        # Connect button signal
        self.button_browseOutputPath.clicked.connect(self.browseOutputPath)

        # Create layout and add widgets
        self.layout = QtWidgets.QGridLayout()

        self.layout.addWidget(self.label_outputPath, 0, 0)

        self.layout.addWidget(self.textbox_outputPath, 0, 1)
        self.layout.addWidget(self.button_browseOutputPath, 0, 2)

        self.layout.addWidget(self.checkbox_skipEmptyVerses, 1, 0, 1, -1)

        self.setLayout(self.layout)

    def skipEmptyVersesChanged(self):
        settings.SkipEmptyVerses.setSkipEmptyVerses(
            self.checkbox_skipEmptyVerses.isChecked())

    def browseOutputPath(self):
        temp = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select output path")

        if temp:
            settings.OutputPath.setOutputPath(temp)
            temp = settings.OutputPath.getOutputPath()
            self.textbox_outputPath.setText(temp)


def showGUI():
    app = QtWidgets.QApplication([])

    main_app = LyricsGeneratorApp()
    main_app.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    showGUI()
