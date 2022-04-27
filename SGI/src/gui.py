from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from ObjectWindow import ObjectWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton

import sys

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.window()

    def window(self) -> None:
        self.resize(700, 600)
        self.setWindowTitle("SGI 1.1: Arthur Milanez e Tiago Possenti")
        layout = QHBoxLayout()
        layout.addLayout(self.menu_setup())
        self.objWindow = ObjectWindow()
        self.setLayout(layout)
        self.show()

    def menu_setup(self) -> QLayout:
        layout = QVBoxLayout()

        layoutObj = QVBoxLayout()
        addObjButton = QPushButton("Adicionar Objeto")
        addObjButton.clicked.connect(self.menu_add_objects)

        objList = QListWidget()

        layoutObj.addWidget(QLabel('Objetos'))
        layoutObj.addWidget(addObjButton)
        layoutObj.addWidget(objList)

        layoutFunctions = QGridLayout()

        up = QToolButton()
        down = QToolButton() 
        left = QToolButton() 
        right = QToolButton() 
        up.setText(" up  ")
        down.setText("down ")
        left.setText("left ")
        right.setText("right")
        layoutFunctions.addWidget(up, 0, 1, Qt.Alignment())
        layoutFunctions.addWidget(down, 2, 1, Qt.Alignment())
        layoutFunctions.addWidget(left, 1, 0, Qt.Alignment())
        layoutFunctions.addWidget(right, 1, 2, Qt.Alignment())

        zoomIn = QToolButton()
        zoomOut = QToolButton()
        zoomIn.setText("zoom in") 
        zoomOut.setText("zoom out")
        layoutFunctions.addWidget(zoomIn, 3, 0, Qt.Alignment())
        layoutFunctions.addWidget(zoomOut, 3, 2, Qt.Alignment()) 

        layout.addLayout(layoutObj)
        layout.addLayout(layoutFunctions)
        return layout 
        
        
    def menu_add_objects(self):
        self.objWindow.exec()

        # addObjWindow = QApplication([])
        # addObjWindow.resize(100, 100)
        # addObjWindow.setWindowTitle("Adicionar Objetos")
        # layout = QHBoxLayout()
        # layout.addLayout(self.menu_setup())
        # self.setLayout(layout)    
        # addObjWindow.show()
        
        

