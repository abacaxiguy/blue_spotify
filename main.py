from pycaw.pycaw import AudioUtilities                   

import ctypes


def mute_spotify():

    windows = ctypes.windll.user32.EnumWindows    
    proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    get_window_text = ctypes.windll.user32.GetWindowTextW
    get_window_length = ctypes.windll.user32.GetWindowTextLengthW
    is_window_visible = ctypes.windll.user32.IsWindowVisible
    titles = []



    def foreach_window(hwnd, lParam):
        if is_window_visible(hwnd):
            length = get_window_length(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            get_window_text(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True

    windows(proc(foreach_window), 0)

    if "Advertisement" in titles:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == "Spotify.exe":
                session.SimpleAudioVolume.SetMute(1, None)

        return False

    if "Spotify" in titles:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == "Spotify.exe":
                session.SimpleAudioVolume.SetMute(1, None)
        return False

    else:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == "Spotify.exe":
                session.SimpleAudioVolume.SetMute(0, None)
        return True


""" MAIN """

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu
from PyQt5 import QtCore
from PyQt5 import QtGui

class App(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)    
        self.trayIcon = QSystemTrayIcon(QtGui.QIcon('icon.ico'))
        self.trayIcon.setToolTip('Blue Spotify is running')

        self.menu = QMenu()
        self.exitAction = self.menu.addAction('Exit 👋')
        self.exitAction.setIcon(QtGui.QIcon('icon.ico'))
        self.exitAction.triggered.connect(sys.exit)

        self.trayIcon.setContextMenu(self.menu)

        timer = QtCore.QTimer(self)

        timer.timeout.connect(self.mute_action)
        timer.start(1000)

    def mute_action(self):
        response = mute_spotify()
        if response:
            self.trayIcon.setToolTip('Blue Spotify is not muting 🔈')
        else:
            self.trayIcon.setToolTip('Blue Spotify is MUTING ✋')




if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = App()
    app.trayIcon.show()
    qt.exec_()
