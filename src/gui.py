import sys
from PySide6 import QtCore, QtWidgets, QtGui
from lyrics2Images import run


class LyricsGeneratorWidget(QtWidgets.QWidget):
    def getFont(self) -> QtGui.QFont:
        return QtGui.QFont("Arial", 16)

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

       # Verse that's being generated
        self.label_verse = QtWidgets.QLabel("Verse:")
        self.label_verse.setFont(self.getFont())

        self.textbox_verse = QtWidgets.QLineEdit()
        self.textbox_verse.setFont(self.getFont())
        self.textbox_verse.setReadOnly(True)

        self.modelList = QtWidgets.QComboBox()
        self.modelList.addItem("stabilityai/sdxl-turbo")
        self.modelList.addItem("stabilityai/stable-diffusion-2-1")
        self.modelList.addItem("SG161222/Realistic_Vision_V2.0")
        self.modelList.addItem("SG161222/Realistic_Vision_V6.0_B1_noVAE")
        self.modelList.addItem("Lykon/DreamShaper")
        self.modelList.addItem("DGSpitzer/Cyberpunk-Anime-Diffusion")
        self.modelList.setFont(self.getFont())

        self.button_generate = QtWidgets.QPushButton("Generate")
        self.button_generate.setFont(self.getFont())

        songName = self.textbox_songName.text()
        artistName = self.textbox_artistName.text()

        self.button_generate.clicked.connect(self.generate)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.label_songName, 0, 0)
        self.layout.addWidget(self.label_artistName, 1, 0)
        self.layout.addWidget(self.textbox_songName, 0, 1)
        self.layout.addWidget(self.textbox_artistName, 1, 1)
        self.layout.addWidget(self.label_modelList, 2, 0)
        self.layout.addWidget(self.modelList, 2, 1)
        self.layout.addWidget(self.label_verse, 3, 0)
        self.layout.addWidget(self.textbox_verse, 3, 1)
        self.layout.addWidget(self.button_generate, 4, 1)

        self.setLayout(self.layout)

    def generate(self):
        songName = self.textbox_songName.text()
        artistName = self.textbox_artistName.text()

        model_id = self.modelList.currentText()
        num_inference_steps = 50

        run(song_name=songName, artist_name=artistName,
            model_id=model_id, num_inference_steps=num_inference_steps)


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
