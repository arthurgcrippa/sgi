from unicodedata import name
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, QDialogButtonBox

from form import Form
from viewport import Viewport

class ObjectWindow(QDialog):
    def __init__(self, viewport: Viewport) -> None:
        super().__init__()
        self.add_object()
        self.viewport = viewport

    def add_object(self) -> None:
        self.resize(300,300)
        self.setWindowTitle("Adicionar Objetos")
        layout = QVBoxLayout()
        layout.addLayout(self.add_tabs())
        self.setLayout(layout)
        # self.show()

    def add_tabs(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.point_tab(), "Ponto")
        # tabs.addTab(self.tab_setup(), "Linha")
        # tabs.addTab(self.tab_setup(), "Poligono")
        layout.addWidget(tabs)

    def point_tab(self) -> QWidget:
        generalTab = QWidget()
        layout = QVBoxLayout()
        self.name = QLineEdit()
        self.coordinates = QLineEdit("(4,4)")
        self.confirmButton = QPushButton('Confirm', self)
        cancelButton = QPushButton('Cancel')
        self.confirmButton.clicked.connect(self.confirm_button)
        dialogBox = QDialogButtonBox()
        dialogBox.rejected.connect(self.reject) 
        dialogBox.addButton(self.confirmButton, QDialogButtonBox.AcceptRole)
        dialogBox.addButton(cancelButton, QDialogButtonBox.RejectRole)

        layout.addWidget(self.name)
        layout.addWidget(self.coordinates)
        layout.addWidget(dialogBox)
        generalTab.setLayout(layout)
        return generalTab

    def confirm_button(self):
        self.viewport.draw(self.form_setup())

    def form_setup(self) -> Form:
        plaintext = self.coordinates.text()
        print(plaintext)

        if (self.checkString(plaintext)):
            coordList = list()
            coordStingList = plaintext.split(';')
            for coordString in coordStingList:
                x = ''
                y = ''
                for char in coordString:
                    firstArgument = True
                    if (char == '(' or char == ')'):
                        continue
                    if (char == ','):
                        firstArgument = False
                        continue
                    if(firstArgument):
                        x = x + char
                    if(not firstArgument):
                        y = y + char
                x = int(x)
                y = int(y)
                coordList.append((x,y))

            form = Form(self.name, coordList)
            return form

    def checkString(self, plaintext):
        return True

        # layout = QVBoxLayout()
        # self.tabs = QTabWidget()
        # tabsFormLayout = QFormLayout()
        # self.tabs.setLayout(tabsFormLayout)

        # ponto = QWidget()
        # pontoFormLayout = QFormLayout()
        # pontoFormLayout.setVerticalSpacing(15)

        # self.pontoName = QLineEdit()
        # pontoFormLayout.addRow(QLabel("Nome"), self.pontoName)
        # self.pontoCoord = QLineEdit()
        # pontoFormLayout.addRow(QLabel("Coordenadas"), self.pontoCoord)

        # ponto.setLayout(pontoFormLayout)
        # self.tabs.addTab(ponto, 'Ponto')

        # layout.addWidget(self.tabs)


        # linha = QWidget()
        # poligono = QWidget()
