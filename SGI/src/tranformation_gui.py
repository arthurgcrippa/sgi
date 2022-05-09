from cProfile import label
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit, QCheckBox, QDialogButtonBox, QRadioButton

from form import Form
from transformation_control import Transformation_control
from viewport import Viewport
from typing import Tuple

t_coordinate = Tuple[float, float]

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

        # self.tab1 = QWidget()
        self.tab2 = QWidget()
        # self.tab3 = QWidget()

        # tabs.addTab(self.tab1, "Translação")
        tabs.addTab(self.tab2, "Rotação")   
        # tabs.addTab(self.tab3, "Escalonamento")

        # self.tab1.setLayout(self.add_translaction())
        self.tab2.setLayout(self.add_rotation())
        # self.tab3.setLayout(self.add_escalonamento())

        return(tabs)

    # def add_translaction(self) -> QFormLayout:
    #     layout = QFormLayout()

    #     addButton = QPushButton("Adicionar")
    #     pointLine = QLineEdit()

    #     addButton.clicked.connect(lambda: self.create_translaction(1, self.coordinate_setup(pointLine.text()), self.viewport.objectList[(int(self.mainWindow.objList.currentItem().text().split(": ")[1]))]))
    #     layout.addWidget(QLabel('Ângulo de Translação'))
    #     layout.addWidget(pointLine)
    #     layout.addWidget(addButton)
        
    #     return(layout)

    def add_rotation(self) -> QFormLayout:
        layout = QFormLayout()

        originButton = QRadioButton('Rotacionar sobre a origem')
        pointButton = QRadioButton('Rotacionar sobre o ponto')
        objCenterButton = QRadioButton('Rotacionar sobre o centro do objeto')
        addButton = QPushButton("Adicionar")
        degreeLine = QLineEdit()
        pointLine = QLineEdit()

        addButton.clicked.connect(lambda: self.create_rotation(2, self.get_axis(originButton, pointButton, objCenterButton), self.get_degree(degreeLine.text()), self.mainWindow.objList.currentItem()), pointLine.text())
        layout.addWidget(QLabel('Opções de Rotação'))
        layout.addWidget(originButton)
        layout.addWidget(pointButton)
        layout.addWidget(objCenterButton)
        layout.addWidget(QLabel('Ângulo de Rotação'))
        layout.addWidget(degreeLine)
        layout.addWidget(QLabel('Ponto de Rotação'))
        layout.addWidget(pointLine)
        layout.addWidget(addButton)

        return(layout)
        
    # def add_escalonamento(self) -> QFormLayout:
    #     layout = QFormLayout()

    #     addButton = QPushButton("Adicionar")
    #     escaleLine = QLineEdit()

    #     addButton.clicked.connect(lambda: self.create_escaling(3, self.get_escale(escaleLine.text()), self.mainWindow.objList.currentItem()))
    #     layout.addWidget(QLabel('Magnitude de Escalonamento'))
    #     layout.addWidget(escaleLine)
    #     layout.addWidget(addButton)

    #     return(layout)

    def confirm_button(self):
        self.transformation_control.confirm_button()

    # def create_translaction(self, type: int, point_diff: t_coordinate, object: Form):
    #     self.transformation_control.add_transform_translaction(type, point_diff, object)

    def create_rotation(self, type: int, axis: int, degree: float, object: Form, point: str):
        self.transformation_control.add_transform_rotation(type, axis, degree, object, self.coordinate_setup(point))

    # def create_escaling(self, type: int, escale: int, object: Form):
    #     self.transformation_control.add_transform_escaling(type, escale, object)

    def get_degree(self, text: str) -> float:
        if text != "":
            return float(text)
        return 1 #TODO
    
    # def get_escale(self, text: str) -> int:
    #     if text != "":
    #         return int(text)
    #     return 1 #TODO

    def get_axis(self, originButton: QRadioButton, pointButton: QRadioButton, objCenterButton: QRadioButton) -> int:
        if originButton.isChecked():
            return 1
        elif pointButton.isChecked():
            return 2
        elif objCenterButton.isChecked():
            return 3
        return 0

    def coordinate_setup(self, coordenate: str) -> t_coordinate:
        if coordenate != "":
            plaintext = coordenate
            if (self.check(plaintext)):
                coordinates = plaintext.split(';')
                for coordinate in coordinates:
                    coordinate = coordinate.replace("(", "")
                    coordinate = coordinate.replace(")", "")
                    xy = coordinate.split(',')
                    x = int(xy[0])
                    y = int(xy[1])
                return (x, y)
            return (0,0)

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
    

        

