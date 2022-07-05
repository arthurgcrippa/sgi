from cProfile import label
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit, QCheckBox, \
    QDialogButtonBox, QRadioButton, QMessageBox, QButtonGroup

from PyQt5.QtCore import Qt

from model.form import Form
from core.transformation_control import Transformation_control
from model.viewport import Viewport
from typing import List, Tuple

from utils import parser

t_coordinate = Tuple[float, float, float]

class Trasformation(QDialog):
    def __init__(self, viewport: Viewport, mainWindow) -> None:
        super().__init__()
        self.transformation_control = Transformation_control(viewport, self)
        self.viewport = viewport
        self.mainWindow = mainWindow
        self.add_transform_window()

    def add_transform_window(self) -> None:
        self.resize(400,400)
        self.setWindowTitle("Transformações")
        layout = QVBoxLayout()

        self.confirmButton = QPushButton('Confirm', self)
        cancelButton = QPushButton('Cancel')
        self.confirmButton.clicked.connect(self.confirm_button)
        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject)
        dialogBox.addButton(self.confirmButton, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancelButton, QDialogButtonBox.RejectRole)

        self.transformList = QListWidget()

        layout.addWidget(self.add_tabs())
        layout.addWidget(self.transformList)
        layout.addWidget(dialogBox)

        self.setLayout(layout)

    def add_tabs(self) -> QTabWidget:
        tabs = QTabWidget()

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        tabs.addTab(self.tab1, "Translação")
        tabs.addTab(self.tab2, "Rotação")
        tabs.addTab(self.tab3, "Escalonamento")

        self.tab1.setLayout(self.add_translaction())
        self.tab2.setLayout(self.add_rotation())
        self.tab3.setLayout(self.add_scaling())

        return(tabs)

    def add_translaction(self) -> QFormLayout:
        layout = QFormLayout()
        addButton = QPushButton("Adicionar")
        diffLine = QLineEdit("(10,10,10)")
        addButton.clicked.connect(lambda: self.create_translaction(1, diffLine.text(), self.get_object()))
        layout.addWidget(QLabel('Ponto de Translação'))
        layout.addWidget(diffLine)
        layout.addWidget(addButton)

        return(layout)

    def add_rotation(self) -> QFormLayout:
        layout = QFormLayout()
        layout_axis = QGridLayout()
        originButton = QRadioButton('Rotacionar sobre a origem')
        pointButton = QRadioButton('Rotacionar sobre o ponto')
        objCenterButton = QRadioButton('Rotacionar sobre o centro do objeto')
        objCenterButton.setChecked(True)
        rotation_type_group = QButtonGroup(layout)
        rotation_type_group.addButton(originButton)
        rotation_type_group.addButton(pointButton)
        rotation_type_group.addButton(objCenterButton)
        self.originButton = originButton
        self.pointButton = pointButton
        self.objCenterButton = objCenterButton
        addButton = QPushButton("Adicionar")
        degreeLine = QLineEdit("30")
        pointLine = QLineEdit("(100,100,0)")
        vectorLine = QLineEdit("(1,0,0)")
        axis_group = QButtonGroup(layout_axis)
        axis_x = QRadioButton('x')
        axis_y = QRadioButton('y')
        axis_z = QRadioButton('z')
        vector = QRadioButton('vetor')
        axis_group.addButton(axis_x)
        axis_group.addButton(axis_y)
        axis_group.addButton(axis_z)
        axis_group.addButton(vector)
        vector.setChecked(True)
        self.axis_x = axis_x
        self.axis_y = axis_y
        self.axis_z = axis_z
        self.vector = vector
        addButton.clicked.connect(lambda: self.create_rotation(2,self.get_degree(degreeLine.text()), pointLine.text(), vectorLine.text(), self.get_object()))
        layout.addWidget(QLabel('Opções de Rotação'))
        layout.addWidget(originButton)
        layout.addWidget(pointButton)
        layout.addWidget(objCenterButton)
        layout.addWidget(QLabel('Ângulo de Rotação'))
        layout.addWidget(degreeLine)
        layout.addWidget(QLabel('Ponto de Rotação'))
        layout.addWidget(pointLine)
        layout.addWidget(QLabel('Vetor de Rotação'))
        layout.addWidget(vectorLine)
        layout_axis.addWidget(axis_x, 0, 1, Qt.Alignment())
        layout_axis.addWidget(axis_y, 0, 2, Qt.Alignment())
        layout_axis.addWidget(axis_z, 0, 3, Qt.Alignment())
        layout_axis.addWidget(vector, 0, 4, Qt.Alignment())
        layout.addRow(QLabel(''), layout_axis)
        layout.addWidget(addButton)

        return(layout)

    def add_scaling(self) -> QFormLayout:
        layout = QFormLayout()

        addButton = QPushButton("Adicionar")
        scaleLine = QLineEdit("(2,2,2)")
        addButton.clicked.connect(lambda: self.create_scaling(3, scaleLine.text(), self.get_object()))
        layout.addWidget(QLabel('Magnitude de Escalonamento'))
        layout.addWidget(scaleLine)
        layout.addWidget(addButton)

        return(layout)

    def confirm_button(self):
        self.transformation_control.confirm_button()

    def create_translaction(self, type: int, pointstr: str, object: Form):
        error_message = []
        if parser.malformed_input(pointstr, error_message):
            self.show_error_message(error_message[0])
        else:
            point = self.get_coordinate(pointstr)
            self.transformation_control.add_translaction(type, point, object)

    def create_rotation(self, type: int, degree: float, pointstr: str, vectorstr: str, object: Form):
        error_message = []
        parser.malformed_input(pointstr, error_message)
        parser.malformed_input(vectorstr, error_message)
        if len(error_message) > 0:
            self.show_error_message(error_message[0])
        else:
            point = self.get_rotation_point(pointstr, object)
            vector = self.get_coordinate(vectorstr)
            self.transformation_control.add_rotation(type, degree, point, vector, self.rotate_around_axis(), self.rotate_by_axis(), object)

    def create_scaling(self, type: int, scalestr: str, object: Form):
        error_message = []
        if parser.malformed_input(scalestr, error_message):
            self.show_error_message(error_message[0])
        else:
            scale = self.get_scale(scalestr)
            self.transformation_control.add_scaling(type, scale, object)

    def get_object(self) -> Form:
        return self.viewport.objectList[(int(self.mainWindow.objList.currentItem().text().split(": ")[1]))]

    def rotate_around_axis(self) -> int:
        if self.originButton.isChecked():
            return 1
        elif self.pointButton.isChecked():
            return 2
        elif self.objCenterButton.isChecked():
            return 3
        return 0

    def rotate_by_axis(self) -> int:
        if self.axis_x.isChecked():
            return 1
        elif self.axis_y.isChecked():
            return 2
        elif self.axis_z.isChecked():
            return 3
        elif self.vector.isChecked():
            return 4
        return 0

    def get_coordinate(self, plaintext: str) -> t_coordinate:
        if plaintext == "":
            return (0,0)
        return parser.parse_float(plaintext)[0]

    def get_rotation_point(self, plaintext: str, object: Form) -> t_coordinate:
        if object.tridimentional():
            return parser.parse_float(plaintext)[0]
        else:
            return self.get_rotation_point_2D(plaintext, object)

    def get_rotation_point_2D(self, plaintext: str, object: Form) -> t_coordinate:
        axis = self.get_axis()
        if axis == 3:
            return object.get_center()
        if axis == 1:
            return (0,0)
        if plaintext == "":
            return (0,0)
        return parser.parse_float(plaintext)[0]

    def get_scale(self, plaintext: str) -> t_coordinate:
        if plaintext == "":
            return (1,1,1)
        return parser.parse_float(plaintext)[0]

    def get_degree(self, text: str) -> float:
        if text != "":
            try:
                return float(text)
            except ValueError:
                return 0
        return 0

    def show_error_message(self, error: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle("Error")
        msg.exec_()
