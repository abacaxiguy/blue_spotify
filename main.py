import sys
import mute_spotify as mute
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QGridLayout, QLabel
from PyQt5 import QtCore
from PyQt5 import QtGui

class App(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Blue Spotify')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setFixedSize(370, 200)
        self.cw = QWidget()
        self.grid = QGridLayout(self.cw)

        self.label = QLabel('Not Running')
        self.label.setStyleSheet('color: gray;font-weight:bold;font-size:40px;')
        self.grid.addWidget(self.label, 2, 0, 5, 5)

        self.logo = QLabel()
        self.logo.setPixmap(QtGui.QPixmap("icon.ico"))
        self.grid.addWidget(self.logo, 0, 0, 1, 5)

        self.setCentralWidget(self.cw)

        timer = QtCore.QTimer(self)

        timer.timeout.connect(self.mute_action)
        timer.start(2000)

    def mute_action(self):
        response = mute.mute_spotify()
        if response:
            self.label.setText('NOT MUTING...')
            self.label.setStyleSheet('color: green;font-weight:bold;font-size:40px;')
        else:
            self.label.setText('MUTING...')
            self.label.setStyleSheet('color: red;font-weight:bold;font-size:40px;')




if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = App()
    app.show()
    qt.exec_()
