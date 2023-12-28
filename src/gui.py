import sys
from PySide6 import QtCore, QtWidgets, QtGui
import lyrics2Images


class LyricsGeneratorWidget(QtWidgets.QWidget):
    def getFont(self) -> QtGui.QFont:
        return QtGui.QFont("Arial", 14)

    def __init__(self):
        super().__init__()

        # Labels for song name and artist name
        self.label_songName = QtWidgets.QLabel("Song name:")
        self.label_songName.setFont(self.getFont())

        self.label_artistName = QtWidgets.QLabel("Artist name:")
        self.label_artistName.setFont(self.getFont())

        # Textboxes for song name and artist name
        self.textbox_songName = QtWidgets.QLineEdit()
        self.textbox_songName.setFont(self.getFont())

        self.textbox_artistName = QtWidgets.QLineEdit()
        self.textbox_artistName.setFont(self.getFont())

        # Model list
        self.label_modelList = QtWidgets.QLabel("Model:")
        self.label_modelList.setFont(self.getFont())

        # Number of inference steps
        self.label_numInferenceSteps = QtWidgets.QLabel("Num inference steps:")
        self.label_numInferenceSteps.setFont(self.getFont())

        self.textbox_numInferenceSteps = QtWidgets.QLineEdit()
        self.textbox_numInferenceSteps.setFont(self.getFont())
        self.textbox_numInferenceSteps.setText("50")

       # Verse that's being generated
        self.label_info = QtWidgets.QLabel("Info:")
        self.label_info.setFont(self.getFont())

        self.textbox_info = QtWidgets.QLineEdit()
        self.textbox_info.setFont(self.getFont())
        self.textbox_info.setReadOnly(True)

        # Loading bar
        self.loading_bar = QtWidgets.QProgressBar()
        self.loading_bar.setFont(self.getFont())
        self.loading_bar.setMinimum(0)
        self.loading_bar.setValue(0)

        # Set width to 100% of the parent
        self.loading_bar.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.modelList = QtWidgets.QComboBox()
        self.modelList.addItem("stabilityai/stable-diffusion-2-1")
        self.modelList.addItem("stabilityai/sdxl-turbo")
        self.modelList.addItem("SG161222/Realistic_Vision_V2.0")
        self.modelList.addItem("SG161222/Realistic_Vision_V6.0_B1_noVAE")
        self.modelList.addItem("Lykon/DreamShaper")
        self.modelList.addItem("DGSpitzer/Cyberpunk-Anime-Diffusion")
        self.modelList.setFont(self.getFont())

        self.button_generate = QtWidgets.QPushButton("Generate")
        self.button_generate.setFont(self.getFont())

        self.button_generate.clicked.connect(self.generate)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.label_songName, 1, 0)
        self.layout.addWidget(self.label_artistName, 0, 0)
        self.layout.addWidget(self.textbox_songName, 0, 1)
        self.layout.addWidget(self.textbox_artistName, 1, 1)
        self.layout.addWidget(self.label_modelList, 2, 0)
        self.layout.addWidget(self.modelList, 2, 1)
        self.layout.addWidget(self.label_numInferenceSteps, 3, 0)
        self.layout.addWidget(self.textbox_numInferenceSteps, 3, 1)
        self.layout.addWidget(self.label_info, 4, 0)
        self.layout.addWidget(self.textbox_info, 4, 1)
        # Adjust the column span to -1
        self.layout.addWidget(self.loading_bar, 5, 0, 1, -1)
        self.layout.addWidget(self.button_generate, 6, 0, 1, -1)

        self.setLayout(self.layout)

    def generate(self):
        songName = self.textbox_songName.text()
        artistName = self.textbox_artistName.text()

        model_id = self.modelList.currentText()
        num_inference_steps = int(self.textbox_numInferenceSteps.text())

        # Validate the input
        assert songName and len(songName) > 0, "Song name cannot be empty"
        assert artistName and len(
            artistName) > 0, "Artist name cannot be empty"
        assert num_inference_steps and num_inference_steps > 0 and num_inference_steps < 100, "Number of inference steps must be between 1 and 100"

        lyrics2Images.run(song_name=songName, artist_name=artistName,
                          model_id=model_id, num_inference_steps=num_inference_steps, uiWidget=self)


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
