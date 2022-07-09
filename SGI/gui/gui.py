from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.object_gui import ObjectWindow
from model.viewport import Viewport
from gui.transformation_gui import Trasformation

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout,  QToolButton, QMessageBox, QSpinBox, QLineEdit, QRadioButton

from core import wavefront2D
from core import wavefront3D

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

        openObjButton = QPushButton("Abrir Objeto")
        saveObjButton = QPushButton("Salvar Objeto")
        fileText = QLineEdit("dinomech.obj")
        openObjButton.clicked.connect(lambda: self.open(fileText.text()))
        saveObjButton.clicked.connect(lambda: self.save(fileText.text()))

        self.cs_algorithm = QRadioButton("Coher Sutherland")
        self.lb_algorithm = QRadioButton("Liang Barsky")
        self.cs_algorithm.setChecked(True)
        change_algorithm = QPushButton("Alterar Algoritmo")
        change_algorithm.clicked.connect(lambda: self.change_algorithm())

        self.objList = QListWidget()

        label_arquivos = QLabel('Manipulação de Arquivos')
        label_arquivos.setAlignment(Qt.AlignCenter)
        layoutObj.addWidget(label_arquivos)
        layoutObj.addWidget(openObjButton)
        layoutObj.addWidget(saveObjButton)
        layoutObj.addWidget(fileText)
        layoutObj.addWidget(QLabel(''))
        label_algorithm = QLabel('Algoritmo de clipping')
        label_algorithm.setAlignment(Qt.AlignCenter)
        layoutObj.addWidget(label_algorithm)
        layoutObj.addWidget(self.cs_algorithm)
        layoutObj.addWidget(self.lb_algorithm)
        layoutObj.addWidget(change_algorithm)
        layoutObj.addWidget(QLabel(''))
        label_objetos = QLabel('Objetos')
        label_objetos.setAlignment(Qt.AlignCenter)
        layoutObj.addWidget(label_objetos)
        layoutObj.addWidget(addObjButton)
        layoutObj.addWidget(transformObjButton)
        layoutObj.addWidget(self.objList)
        layoutObj.addWidget(QLabel(''))
        label_movimento = QLabel('Movimentações')
        label_movimento.setAlignment(Qt.AlignCenter)
        layoutObj.addWidget(label_movimento)

        layoutFunctions = QGridLayout()

        up = QToolButton()
        down = QToolButton()
        left = QToolButton()
        right = QToolButton()
        up3d = QToolButton()
        down3d = QToolButton()

        up.setFixedSize(100,25)
        down.setFixedSize(100,25)
        left.setFixedSize(100,25)
        right.setFixedSize(100,25)
        up3d.setFixedSize(100, 25)
        down3d.setFixedSize(100, 25)
        self.axis_x = QRadioButton("x")
        self.axis_y = QRadioButton("y")
        self.axis_z = QRadioButton("z")
        self.axis_z.setChecked(True)
        up.setIcon(QtGui.QIcon("images/cima.png"))
        down.setIcon(QtGui.QIcon("images/baixo.png"))
        right.setIcon(QtGui.QIcon("images/drt.png"))
        left.setIcon(QtGui.QIcon("images/sqrd.png"))
        up3d.setIcon(QtGui.QIcon("images/cima.png"))
        down3d.setIcon(QtGui.QIcon("images/baixo.png"))
        layoutFunctions.addWidget(up, 0, 1, Qt.Alignment())
        layoutFunctions.addWidget(down, 2, 1, Qt.Alignment())
        layoutFunctions.addWidget(left, 2, 0, Qt.Alignment())
        layoutFunctions.addWidget(right, 2, 2, Qt.Alignment())
        layoutFunctions.addWidget(up3d, 1, 0, Qt.Alignment())
        layoutFunctions.addWidget(down3d, 1, 2, Qt.Alignment())
        layoutFunctions.addWidget(QLabel("<         3d         >"), 1, 1, Qt.Alignment())
        layoutFunctions.addWidget(self.axis_x, 5, 0, Qt.Alignment())
        layoutFunctions.addWidget(self.axis_y, 5, 1, Qt.Alignment())
        layoutFunctions.addWidget(self.axis_z, 5, 2, Qt.Alignment())
        up.clicked.connect(lambda: self.viewport.move(1))
        down.clicked.connect(lambda: self.viewport.move(2))
        left.clicked.connect(lambda: self.viewport.move(3))
        right.clicked.connect(lambda: self.viewport.move(4))
        up3d.clicked.connect(lambda: self.viewport.move(5))
        down3d.clicked.connect(lambda: self.viewport.move(6))

        zoomIn = QToolButton()
        zoomOut = QToolButton()
        zoomIn.setIcon(QtGui.QIcon("images/mais.png"))
        zoomOut.setIcon(QtGui.QIcon("images/menos.png"))
        zoomIn.setFixedSize(100,25)
        zoomOut.setFixedSize(100,25)
        layoutFunctions.addWidget(zoomIn, 0, 0, Qt.Alignment())
        layoutFunctions.addWidget(zoomOut, 0, 2, Qt.Alignment())
        zoomIn.clicked.connect(lambda: self.viewport.zoom_out())
        zoomOut.clicked.connect(lambda: self.viewport.zoom_in())

        right_rotation = QToolButton()
        left_rotation = QToolButton()
        self.degree_box = QSpinBox()
        self.degree_box.setRange(10, 180)
        self.degree_box.setSingleStep(10)
        right_rotation.setIcon(QtGui.QIcon("images/direita.png"))
        left_rotation.setIcon(QtGui.QIcon("images/esquerda.png"))
        right_rotation.setFixedSize(100,25)
        left_rotation.setFixedSize(100,25)
        layoutFunctions.addWidget(self.degree_box, 4, 1, Qt.Alignment())
        layoutFunctions.addWidget(right_rotation, 4, 2, Qt.Alignment())
        layoutFunctions.addWidget(left_rotation, 4, 0, Qt.Alignment())
        right_rotation.clicked.connect(lambda: self.viewport.rotate_window(self.degree_box.value(), 1, self.get_axis()))
        left_rotation.clicked.connect(lambda: self.viewport.rotate_window(self.degree_box.value(), 0, self.get_axis()))
        layout.addLayout(layoutObj)
        layout.addLayout(layoutFunctions)
        return layout

    def vp_setup(self) -> QLayout:
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Viewport'))
        self.viewport = Viewport(600, 600, 600)
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

    def save(self, file_name: str) -> None:
        wavefront3D.write(file_name, self.viewport.objectList)

    def open(self, file_path: str) -> None:
        self.objList.clear()
        self.viewport.objectList.clear()
        self.viewport.redraw()
        new_objects = wavefront3D.read(file_path)
        for obj in new_objects:
            if obj.IS_WINDOW:
                self.viewport.update_window(obj.coordinates)
            else:
                self.viewport.objectList.append(obj)
                self.objList.addItem(obj.name + ': ' + str(obj.id))
        self.viewport.redraw()

    def get_algorithm(self):
        if self.cs_algorithm.isChecked():
            print("Voce esta usando coher suterland")
            return 1
        else:
            print("Voce esta usando Linag Barsk")
            return 0

    def get_axis(self):
        if self.axis_x.isChecked():
            return 1
        elif self.axis_y.isChecked():
            return 2
        elif self.axis_z.isChecked():
            return 3
        return 0

    def change_algorithm(self):
        self.viewport.clipper.set_algorithm(self.get_algorithm())
