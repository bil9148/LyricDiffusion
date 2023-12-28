import sys
from PySide6 import QtCore, QtWidgets, QtGui


class LyricsGeneratorWidget(QtWidgets.QWidget):
    def getFont(self) -> QtGui.QFont:
        return QtGui.QFont("Arial", 16)

    def __init__(self):
        super().__init__()

        self.label_songName = QtWidgets.QLabel("Song name:")
        self.label_songName.setFont(self.getFont())

        self.label_artistName = QtWidgets.QLabel("Artist name:")
        self.label_artistName.setFont(self.getFont())

        self.textbox_songName = QtWidgets.QLineEdit()
        self.textbox_songName.setFont(self.getFont())

        self.textbox_artistName = QtWidgets.QLineEdit()
        self.textbox_artistName.setFont(self.getFont())

        self.button_generate = QtWidgets.QPushButton("Generate")
        self.button_generate.setFont(self.getFont())

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.label_songName, 0, 0,
                              QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.textbox_songName, 0,
                              1, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label_artistName, 1,
                              0, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.textbox_artistName, 1,
                              1, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.button_generate, 2, 0,
                              1, 2, QtCore.Qt.AlignCenter)

        self.setLayout(self.layout)


class LyricsGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = LyricsGeneratorWidget()
        self.setCentralWidget(self.central_widget)

        self.resize(600, 400)
        self.setWindowTitle("Lyrics2Images")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    main_app = LyricsGeneratorApp()
    main_app.show()

    sys.exit(app.exec())
