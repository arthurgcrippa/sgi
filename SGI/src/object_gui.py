#from unicodedata import name
#from PyQt5.QtCore import Qt
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, QDialogButtonBox

from form import Form
from viewport import Viewport
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
        layout.addLayout(self.add_tabs())
        self.setLayout(layout)

    def add_tabs(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        self.setLayout(layout)
        tabs = QTabWidget()
        tabs.addTab(self.object_tab(), "Objeto")
        layout.addWidget(tabs)

    def object_tab(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.name = QLineEdit("Nome do Objeto")
        self.coordinates_tab = QLineEdit("(-50,1);(1,1);(1,50);(-50,50)")
        self.confirmButton = QPushButton('Confirm', self)
        cancelButton = QPushButton('Cancel')
        self.confirmButton.clicked.connect(self.confirm_button)
        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject)
        dialogBox.addButton(self.confirmButton, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancelButton, QDialogButtonBox.RejectRole)

        layout.addWidget(self.name)
        layout.addWidget(self.coordinates_tab)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def confirm_button(self):
        form = self.form_setup()
        self.viewport.objectList.append(form)
        self.viewport.draw(form)
        self.mainWindow.objList.addItem(form.name + ': ' + str(form.id))

    def form_setup(self) -> Form:
        coordinatesList = list()
        plaintext = self.coordinates_tab.text()
        if (self.check(plaintext)):
            coordinates = plaintext.split(';')
            for coordinate in coordinates:
                coordinate = coordinate.replace("(", "")
                coordinate = coordinate.replace(")", "")
                xy = coordinate.split(',')
                x = int(xy[0])
                y = int(xy[1])
                coordinatesList.append((x,y))
            form = Form(self.name.text(), coordinatesList, len(self.viewport.objectList))
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
                print(2)
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
