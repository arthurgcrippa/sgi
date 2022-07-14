from cProfile import label
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QRadioButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, \
    QDialogButtonBox, QMessageBox, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt
from utils import matrices
from model.form import Form
from model.object2D import Object2D
from model.object3D import Object3D
from model.viewport import Viewport

from utils import parser

class ObjectWindow(QDialog):
    def __init__(self, viewport: Viewport, mainWindow) -> None:
        super().__init__()
        self.add_object_window()
        self.viewport = viewport
        self.mainWindow = mainWindow

    def add_object_window(self) -> None:
        self.resize(400,300)
        self.setWindowTitle("Adicionar Objetos")
        layout = QVBoxLayout()
        layout.addWidget(self.add_tabs())
        self.setLayout(layout)

    def add_tabs(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.addTab(self.object_tab_2D(), "Objeto 2D")
        tabs.addTab(self.object_tab_3D(), "Objeto 3D")
        tabs.addTab(self.curve_tab(), "Curva")
        tabs.addTab(self.surface_tab(), "Superficie")
        return tabs

    def object_tab_2D(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.object_name_2D = QLineEdit("Nome do Objeto")
        self.object_coordinates_2D = QLineEdit("(-50,1);(1,1);(1,50);(-50,50)")
        self.object_color_2D = QLineEdit("#000000")
        self.is_poligon_2D = QCheckBox("Fill object")
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
        layout.addWidget(self.is_poligon_2D)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def object_tab_3D(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.object_name_3D = QLineEdit("Nome do Objeto")
        #self.object_coordinates = QLineEdit("(-50,1,10);(1,1,10);(1,50,10);(-50,50,10)")
        self.object_coordinates_3D = QLineEdit("(-50,0,-50);(-50,0,50);(50,0,50);(50,0,-50);(0,100,0)")
        #self.object_edges = QLineEdit("(1,2);(2,3);(3,4);(4,1);(1,5);(2,5);(3,5);(4,5)")
        self.object_edges = QLineEdit("(1,2,3,4,1);(1,5,2);(3,5,4)")
        #self.object_coordinates = QLineEdit("(10,10,10)")
        #self.object_edges = QLineEdit("(1,1)")
        self.object_color_3D = QLineEdit("#000000")
        self.is_poligon_3D = QCheckBox("Fill object")
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
        layout.addWidget(self.is_poligon_3D)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def curve_tab(self) -> QWidget:
        generalTab = QWidget()
        layout = QFormLayout()
        algo_options_layout = QGridLayout()
        method_options_layout = QGridLayout()

        algo_options_group = QButtonGroup(algo_options_layout)
        method_options_group = QButtonGroup(method_options_layout)

        self.curve_name = QLineEdit("Nome da Curva")
        self.curve_coordinates = QLineEdit("(-100,-100,-100);(-50,-150,-50);(-50,150,50);(1,1,1);(50,50,50);(50,100,50);(100,100,100)")
        self.curve_color = QLineEdit("#000000")
        self.bezier_button = QRadioButton('Bezier')
        self.hermite_button = QRadioButton('Hermite')
        self.bspline_button = QRadioButton('B-Spline')
        self.curve_blending_button = QRadioButton('Blending Functions')
        self.curve_forwarding_button = QRadioButton('Forwarding Differences')

        self.bezier_button.setChecked(True)
        self.curve_blending_button.setChecked(True)

        method_options_group.addButton(self.bezier_button)
        method_options_group.addButton(self.hermite_button)
        method_options_group.addButton(self.bspline_button)
        algo_options_group.addButton(self.curve_blending_button)
        algo_options_group.addButton(self.curve_forwarding_button)

        algo_options_layout.addWidget(self.curve_blending_button, 1, 1, Qt.Alignment())
        algo_options_layout.addWidget(self.curve_forwarding_button, 1, 2, Qt.Alignment())
        method_options_layout.addWidget(self.bezier_button, 0, 1, Qt.Alignment())
        method_options_layout.addWidget(self.hermite_button, 0, 2, Qt.Alignment())
        method_options_layout.addWidget(self.bspline_button, 0, 3, Qt.Alignment())

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
        layout.addRow(QLabel(''), method_options_layout)
        layout.addRow(QLabel(''), algo_options_layout)
        layout.addRow(QLabel(''), QVBoxLayout())
        layout.addRow(QLabel(''), QVBoxLayout())
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def surface_tab(self) -> QWidget:
        generalTab = QWidget()
        layout = QFormLayout()
        algo_options_layout = QGridLayout()
        method_options_layout = QGridLayout()

        algo_options_group = QButtonGroup(algo_options_layout)
        method_options_group = QButtonGroup(method_options_layout)

        self.surface_name = QLineEdit("Nome da Superficie")
        self.surface_coordinates = QLineEdit("(0,0,0);(0,30,40);(0,60,30);(0,100,0);(30,0,20);(20,25,50);(30,60,50);(40,80,20);(60,0,20);(80,30,50);(70,60,45);(60,100,25);(100,0,0);(110,30,40);(110,60,30);(100,90,0)")
        self.surface_color = QLineEdit("#000000")
        self.bezier_surface_button = QRadioButton('Bezier')
        self.hermite_surface_button = QRadioButton('Hermite')
        self.bspline_surface_button = QRadioButton('B-Spline')
        self.surface_blending_button = QRadioButton('Blending Functions')
        self.surface_forwarding_button = QRadioButton('Forwarding Differences')

        self.bezier_surface_button.setChecked(True)
        self.surface_blending_button.setChecked(True)

        method_options_group.addButton(self.bezier_surface_button)
        method_options_group.addButton(self.hermite_surface_button)
        method_options_group.addButton(self.bspline_surface_button)
        algo_options_group.addButton(self.surface_blending_button)
        algo_options_group.addButton(self.surface_forwarding_button)

        algo_options_layout.addWidget(self.surface_blending_button, 1, 1, Qt.Alignment())
        algo_options_layout.addWidget(self.surface_forwarding_button, 1, 2, Qt.Alignment())
        method_options_layout.addWidget(self.bezier_surface_button, 0, 1, Qt.Alignment())
        method_options_layout.addWidget(self.hermite_surface_button, 0, 2, Qt.Alignment())
        method_options_layout.addWidget(self.bspline_surface_button, 0, 3, Qt.Alignment())

        confirm_button = QPushButton('Confirm', self)
        cancel_button = QPushButton('Cancel')
        confirm_button.clicked.connect(self.confirm_surface)

        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject)
        dialogBox.addButton(confirm_button, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancel_button, QDialogButtonBox.RejectRole)

        layout.addWidget(self.surface_name)
        layout.addWidget(self.surface_coordinates)
        layout.addWidget(self.surface_color)
        layout.addRow(QLabel(''), method_options_layout)
        layout.addRow(QLabel(''), algo_options_layout)
        layout.addRow(QLabel(''), QVBoxLayout())
        layout.addRow(QLabel(''), QVBoxLayout())
        # layout.addWidget(self.bezier_surface_button)
        # layout.addWidget(self.hermite_surface_button)
        # layout.addWidget(self.bspline_surface_button)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab


    def confirm_object(self, object: Form, FLAG_3D: bool):
        object.set_color(self.get_color(object).text(), 0)
        object.set_as_polygon(self.is_polygon(object))
        if FLAG_3D:
            error_code = []
            if not parser.malformed_input(self.object_edges.text(), error_code):
                self.show_error_message(error_code[0])
                return
            else:
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
            #matrices.rotation_test(object)


    def confirm_curve(self):
        error_message = []
        if parser.malformed_input(self.curve_coordinates.text(), error_message):
            self.show_error_message(error_message[0])
        else:
            object = self.form_setup_3D(self.curve_name.text(), self.curve_coordinates.text())
            object.set_as_curve(True)
            if self.hermite_button.isChecked():
                object.set_curve_type(1)
            if self.bezier_button.isChecked():
                object.set_curve_type(2)
            if self.curve_blending_button.isChecked():
                object.set_curve_algorythm(1)
            if self.curve_forwarding_button.isChecked():
                object.set_curve_algorythm(0)
            self.confirm_object(object, True)

    def confirm_surface(self):
        error_message = []
        if parser.malformed_input(self.surface_coordinates.text(), error_message):
            self.show_error_message(error_message[0])
        else:
            object = self.form_setup_3D(self.surface_name.text(), self.surface_coordinates.text())
            object.set_as_surface(True)
            if self.hermite_surface_button.isChecked():
                object.set_surface_type(1)
            if self.bezier_surface_button.isChecked():
                object.set_surface_type(2)
            if self.surface_blending_button.isChecked():
                object.set_surface_algorythm(0)
            if self.surface_forwarding_button.isChecked():
                object.set_surface_algorythm(1)
            self.confirm_object(object, True)

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

    def is_polygon(self, object: Form):
        if object.tridimentional():
            return self.is_poligon_3D.isChecked()
        else:
            return self.is_poligon_2D.isChecked()

    def get_color(self, object: Form):
        if object.tridimentional():
            return self.object_color_3D
        else:
            return self.object_color_2D


    def get_edges(self):
        plaintext = self.object_edges.text()
        edges = parser.parse_edges(plaintext)
        return edges
