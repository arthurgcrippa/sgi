from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox

import sys

class ObjectWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.add_object()

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
        tabs.addTab(self.tab_setup(), "Ponto")
        tabs.addTab(self.tab_setup(), "Linha")
        tabs.addTab(self.tab_setup(), "Poligono")
        layout.addWidget(tabs)

    def tab_setup(self):
        generalTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLineEdit("Nome do Objeto"))
        layout.addWidget(QLineEdit("Coordenada"))
        generalTab.setLayout(layout)
        return generalTab

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



