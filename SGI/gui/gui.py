from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.object_gui import ObjectWindow
from model.viewport import Viewport
from gui.transformation_gui import Trasformation

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QMessageBox

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.window()

    def window(self) -> None:
        self.resize(700, 600)
        self.setWindowTitle("SGI 1.1: Arthur Milanez e Tiago Possenti")
        layout = QHBoxLayout()
        layout.addLayout(self.menu_setup())
        layout.addLayout(self.vp_setup())
        self.objWindow = ObjectWindow(self.viewport, self)
        self.transformation = Trasformation(self.viewport, self)
        self.setLayout(layout)
        self.show()

    def menu_setup(self) -> QLayout:
        layout = QVBoxLayout()

        layoutObj = QVBoxLayout()
        addObjButton = QPushButton("Adicionar Objeto")
        addObjButton.clicked.connect(self.menu_add_objects)

        transformObjButton = QPushButton("Transformar Objeto")
        transformObjButton.clicked.connect(self.menu_tranformations)

        self.objList = QListWidget()

        layoutObj.addWidget(QLabel('Objetos'))
        layoutObj.addWidget(addObjButton)
        layoutObj.addWidget(transformObjButton)
        layoutObj.addWidget(self.objList)

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
        up.clicked.connect(lambda: self.viewport.move(1))
        down.clicked.connect(lambda: self.viewport.move(2))
        left.clicked.connect(lambda: self.viewport.move(3))
        right.clicked.connect(lambda: self.viewport.move(4))

        zoomIn = QToolButton()
        zoomOut = QToolButton()
        zoomIn.setText("zoom in")
        zoomOut.setText("zoom out")
        layoutFunctions.addWidget(zoomIn, 3, 0, Qt.Alignment())
        layoutFunctions.addWidget(zoomOut, 3, 2, Qt.Alignment())
        zoomIn.clicked.connect(lambda: self.viewport.zoom_out())
        zoomOut.clicked.connect(lambda: self.viewport.zoom_in())

        right_rotation = QToolButton()
        left_rotation = QToolButton()
        right_rotation.setText("right rotation")
        left_rotation.setText("left rotation")
        layoutFunctions.addWidget(right_rotation, 0, 2, Qt.Alignment())
        layoutFunctions.addWidget(left_rotation, 0, 0, Qt.Alignment())
        right_rotation.clicked.connect(lambda: self.viewport.zoom_out())
        left_rotation.clicked.connect(lambda: self.viewport.zoom_in())


        layout.addLayout(layoutObj)
        layout.addLayout(layoutFunctions)
        return layout

    def vp_setup(self) -> QLayout:
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Viewport'))
        self.viewport = Viewport(500, 500)
        layout.addWidget(self.viewport)
        return layout

    def menu_add_objects(self):
        self.objWindow.exec()

    def show_error_message(self, error: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle("Error")
        msg.exec_()

    def menu_tranformations(self):
        if(self.objList.currentItem() == None):
            self.show_error_message("Você nao selecionou nenhum objeto da lista")
        else:
            self.transformation.exec()
