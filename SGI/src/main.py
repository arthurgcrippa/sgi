from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton

import sys

from gui.gui import MainWindow

def main():
    app = QApplication([])
    window = MainWindow()
    app.exec()

if __name__ == '__main__':
    main()

