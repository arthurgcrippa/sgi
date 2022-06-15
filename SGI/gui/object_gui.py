#from unicodedata import name
#from PyQt5.QtCore import Qt
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QRadioButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, QDialogButtonBox

from model.form import Form
from model.viewport import Viewport
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
        tabs.addTab(self.object_tab(), "Objeto")
        tabs.addTab(self.curve_tab(), "Curva")
        return tabs

    def object_tab(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.object_name = QLineEdit("Nome do Objeto")
        #self.object_coordinates = QLineEdit("(-50,1,10);(1,1,10);(1,50,10);(-50,50,10)")
        self.object_coordinates = QLineEdit("(-50,0,-50);(-50,0,50);(50,0,50);(50,0,-50);(0,100,0)")
        self.object_edges = QLineEdit("(1,2);(2,3);(3,4);(4,1);(1,5);(2,5);(3,5);(4,5)")
        #self.object_coordinates = QLineEdit("(10,10,10)")
        #self.object_edges = QLineEdit("(1,1)")
        self.object_color = QLineEdit("#000000")
        self.fill_poligon = QCheckBox("Fill object")
        self.confirmButton = QPushButton('Confirm', self)
        cancelButton = QPushButton('Cancel')
        self.confirmButton.clicked.connect(self.confirm_object)
        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject)
        dialogBox.addButton(self.confirmButton, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancelButton, QDialogButtonBox.RejectRole)

        layout.addWidget(self.object_name)
        layout.addWidget(self.object_coordinates)
        layout.addWidget(self.object_edges)
        layout.addWidget(self.object_color)
        layout.addWidget(self.fill_poligon)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def curve_tab(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.curve_name = QLineEdit("Nome da Curva")
        self.curve_coordinates = QLineEdit("(-100,-100);(-50,-150);(-50,150);(1,1);(50,50);(50,100);(100,100)")
        self.curve_color = QLineEdit("#000000")
        self.bezierButton = QRadioButton('Bezier')
        self.hermiteButton = QRadioButton('Hermite')
        self.bsplineButton = QRadioButton('B-Spline')
        confirmButton = QPushButton('Confirm', self)
        cancelButton = QPushButton('Cancel')
        confirmButton.clicked.connect(self.confirm_curve)
        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject)
        dialogBox.addButton(confirmButton, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancelButton, QDialogButtonBox.RejectRole)

        layout.addWidget(self.curve_name)
        layout.addWidget(self.curve_coordinates)
        layout.addWidget(self.curve_color)
        layout.addWidget(self.bezierButton)
        layout.addWidget(self.hermiteButton)
        layout.addWidget(self.bsplineButton)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab


    def confirm_object(self):
        form = self.form_setup(self.object_name.text(), self.object_coordinates.text())
        form.set_color(self.object_color.text(), 0)
        form.set_fill(self.check_fill())
        form.set_edges(self.check_edges())
        self.viewport.objectList.append(form)
        self.viewport.draw(form)
        self.mainWindow.objList.addItem(form.name + ': ' + str(form.id))

    def confirm_curve(self):
        form = self.form_setup(self.curve_name.text(), self.curve_coordinates.text())
        form.set_curvy(True)
        form.set_color(self.curve_color.text(), 0)
        if self.hermiteButton.isChecked():
            form.set_curve_type(1)
        if self.bezierButton.isChecked():
            form.set_curve_type(2)
        self.viewport.objectList.append(form)
        self.viewport.draw(form)
        self.mainWindow.objList.addItem(form.name + ': ' + str(form.id))

    def form_setup(self, name, coordinates_text) -> Form:
        coordinatesList = list()
        plaintext = coordinates_text
        if (self.check(plaintext)):
            coordinates = plaintext.split(';')
            for coordinate in coordinates:
                coordinate = coordinate.replace("(", "")
                coordinate = coordinate.replace(")", "")
                xyz = coordinate.split(',')
                x = int(xyz[0])
                y = int(xyz[1])
                z = int(xyz[2])
                coordinatesList.append((x,y,z))
            form = Form(name, coordinatesList, len(self.viewport.objectList))
            return form

    def check(self, plaintext):
        stack = []
        prev = ''
        for char in plaintext:
            if len(stack) > 0:
               prev = stack.pop()
            if not (self.isOperator(char) or char.isnumeric()):
                return False
            stack.append(char)
            if prev == '(' and ((not char.isnumeric()) and char != '-'):
                return False
            if prev == ')' and char != ';':
                return False
            if prev == '-' and (char == '(' or char == ')'):
                return False
        return True

    def isOperator(self, char):
        if (char == '(' or char == ')' or char == ',' or char == ';' or char == '-'):
            return True
        return False

    def check_fill(self):
        if self.fill_poligon.isChecked():
            return True
        else:
            return False

    def check_edges(self):
        plaintext = self.object_edges.text()
        coordinates = plaintext.split(";")
        edges = list()
        for coordinate in coordinates:
            coordinate = coordinate.replace("(", "").replace(")", "")
            coordinate_text = coordinate.split(",")
            edge = (int(coordinate_text[0]), int(coordinate_text[1]))
            edges.append(edge)
        return edges
