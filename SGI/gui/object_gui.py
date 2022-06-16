#from unicodedata import name
#from PyQt5.QtCore import Qt
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QRadioButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, \
    QDialogButtonBox, QMessageBox

from model.form import Form
from model.object2D import Object2D
from model.object3D import Object3D
from model.viewport import Viewport

from utils import parser
# from gui import MainWindow

class ObjectWindow(QDialog):
    def __init__(self, viewport: Viewport, mainWindow) -> None:
        super().__init__()
        self.add_object_window()
        self.viewport = viewport
        self.mainWindow = mainWindow

    def add_object_window(self) -> None:
        self.resize(300,300)
        self.setWindowTitle("Adicionar Objetos")
        layout = QVBoxLayout()
        layout.addWidget(self.add_tabs())
        self.setLayout(layout)

    def add_tabs(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.addTab(self.object_tab_2D(), "Objeto 2D")
        tabs.addTab(self.object_tab_3D(), "Objeto 3D")
        tabs.addTab(self.curve_tab(), "Curva")
        return tabs

    def object_tab_2D(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.object_name_2D = QLineEdit("Nome do Objeto")
        self.object_coordinates_2D = QLineEdit("(-50,1);(1,1);(1,50);(-50,50)")
        self.object_color_2D = QLineEdit("#000000")
        self.fill_poligon_2D = QCheckBox("Fill object")
        self.confirm_button_2D = QPushButton('Confirm', self)
        cancel_button = QPushButton('Cancel')
        self.confirm_button_2D.clicked.connect(self.confirm_object_2D)
        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject)
        dialogBox.addButton(self.confirm_button_2D, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancel_button, QDialogButtonBox.RejectRole)

        layout.addWidget(self.object_name_2D)
        layout.addWidget(self.object_coordinates_2D)
        layout.addWidget(self.object_color_2D)
        layout.addWidget(self.fill_poligon_2D)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def object_tab_3D(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.object_name_3D = QLineEdit("Nome do Objeto")
        #self.object_coordinates = QLineEdit("(-50,1,10);(1,1,10);(1,50,10);(-50,50,10)")
        self.object_coordinates_3D = QLineEdit("(-50,0,-50);(-50,0,50);(50,0,50);(50,0,-50);(0,100,0)")
        self.object_edges = QLineEdit("(1,2);(2,3);(3,4);(4,1);(1,5);(2,5);(3,5);(4,5)")
        #self.object_coordinates = QLineEdit("(10,10,10)")
        #self.object_edges = QLineEdit("(1,1)")
        self.object_color_3D = QLineEdit("#000000")
        self.fill_poligon_3D = QCheckBox("Fill object")
        self.confirm_button_3D = QPushButton('Confirm', self)
        cancel_button = QPushButton('Cancel')
        self.confirm_button_3D.clicked.connect(self.confirm_object_3D)
        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject)
        dialogBox.addButton(self.confirm_button_3D, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancel_button, QDialogButtonBox.RejectRole)

        layout.addWidget(self.object_name_3D)
        layout.addWidget(self.object_coordinates_3D)
        layout.addWidget(self.object_edges)
        layout.addWidget(self.object_color_3D)
        layout.addWidget(self.fill_poligon_3D)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def curve_tab(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.curve_name = QLineEdit("Nome da Curva")
        self.curve_coordinates = QLineEdit("(-100,-100,-100);(-50,-150,-50);(-50,150,50);(1,1,1);(50,50,50);(50,100,50);(100,100,100)")
        self.curve_color = QLineEdit("#000000")
        self.bezier_button = QRadioButton('Bezier')
        self.hermite_button = QRadioButton('Hermite')
        self.bspline_button = QRadioButton('B-Spline')
        confirm_button = QPushButton('Confirm', self)
        cancel_button = QPushButton('Cancel')
        confirm_button.clicked.connect(self.confirm_curve)
        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject)
        dialogBox.addButton(confirm_button, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancel_button, QDialogButtonBox.RejectRole)

        layout.addWidget(self.curve_name)
        layout.addWidget(self.curve_coordinates)
        layout.addWidget(self.curve_color)
        layout.addWidget(self.bezier_button)
        layout.addWidget(self.hermite_button)
        layout.addWidget(self.bspline_button)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def confirm_object(self, object: Form, FLAG_3D: bool):
        object.set_color(self.get_color(object).text(), 0)
        object.set_fill(self.get_fill(object))
        if FLAG_3D:
            object.set_edges(self.get_edges())
        self.viewport.objectList.append(object)
        self.viewport.draw(object)
        self.mainWindow.objList.addItem(object.name + ': ' + str(object.id))

    def confirm_object_2D(self):
        error_message = []
        if parser.malformed_input(self.object_coordinates_2D.text(), error_message):
            self.show_error_message(error_message[0])
        else:
            object = self.form_setup_2D(self.object_name_2D.text(), self.object_coordinates_2D.text())
            self.confirm_object(object, False)

    def confirm_object_3D(self):
        error_message = []
        if parser.malformed_input(self.object_coordinates_3D.text(), error_message):
            self.show_error_message(error_message[0])
        else:
            object = self.form_setup_3D(self.object_name_3D.text(), self.object_coordinates_3D.text())
            self.confirm_object(object, True)


    def confirm_curve(self):
        error_message = []
        if parser.malformed_input(self.curve_coordinates.text(), error_message):
            self.show_error_message(error_message[0])
        else:
            object = self.form_setup_3D(self.curve_name.text(), self.curve_coordinates.text())
            object.set_curvy(True)
            if self.hermite_button.isChecked():
                object.set_curve_type(1)
            if self.bezier_button.isChecked():
                object.set_curve_type(2)
            self.confirm_object(object, False)

    def form_setup(self, plaintext):
        coordinates = parser.parse_float(plaintext)
        return coordinates

    def form_setup_2D(self, name, plaintext) -> Form:
        coordinates = self.form_setup(plaintext)
        object = Object2D(name, coordinates, len(self.viewport.objectList))
        return object

    def form_setup_3D(self, name, plaintext) -> Form:
        coordinates = self.form_setup(plaintext)
        object = Object3D(name, coordinates, len(self.viewport.objectList))
        return object

    def show_error_message(self, error: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle("Error")
        msg.exec_()

    def get_fill(self, object: Form):
        if object.tridimentional():
            return self.fill_poligon_3D.isChecked()
        else:
            return self.fill_poligon_2D.isChecked()

    def get_color(self, object: Form):
        if object.tridimentional():
            return self.object_color_3D
        else:
            return self.object_color_2D


    def get_edges(self):
        plaintext = self.object_edges.text()
        edges = parser.parse_int(plaintext)
        return edges
