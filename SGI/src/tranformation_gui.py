from cProfile import label
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit, QCheckBox, QDialogButtonBox, QRadioButton

from form import Form
from transformation_control import Transformation_control
from viewport import Viewport

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
        self.tab3.setLayout(self.add_escalonamento())

        return(tabs)

    def add_translaction(self) -> QFormLayout:
        layout = QFormLayout()

        originButton = QRadioButton('Transladar sobre a origem')
        pointButton = QRadioButton('Transladar sobre o ponto')
        objCenterButton = QRadioButton('Transladar sobre o centro do objeto')
        addButton = QPushButton("Adicionar")
        degreeLine = QLineEdit()

        # axis = self.get_axis(originButton, pointButton, objCenterButton)
        # # degree = float(degreeLine.text())
        # degree = self.get_degree(degreeLine.text())
        # object = self.mainWindow.objList.currentItem()

        addButton.clicked.connect(lambda: self.add_transform(1,self.get_axis(originButton, pointButton, objCenterButton),\
                                     self.get_degree(degreeLine.text()), self.viewport.objectList[(int(self.mainWindow.objList.currentItem().text().split(": ")[1]))]))

        layout.addWidget(QLabel('Opções de Translação'))
        layout.addWidget(originButton)
        layout.addWidget(pointButton)
        layout.addWidget(objCenterButton)
        layout.addWidget(QLabel('Ângulo de Translação'))
        layout.addWidget(degreeLine)
        layout.addWidget(addButton)
        
        return(layout)

    def add_rotation(self) -> QFormLayout:
        layout = QFormLayout()

        originButton = QRadioButton('Rotacionar sobre a origem')
        pointButton = QRadioButton('Rotacionar sobre o ponto')
        objCenterButton = QRadioButton('Rotacionar sobre o centro do objeto')
        addButton = QPushButton("Adicionar")
        degreeLine = QLineEdit()

        # axis = self.get_axis(originButton, pointButton, objCenterButton)
        # degree = float(degreeLine.text())
        # degree = self.get_degree(degreeLine.text())
        # object = self.mainWindow.objList.currentItem()

        addButton.clicked.connect(lambda: self.add_transform(2,self.get_axis(originButton, pointButton, objCenterButton),\
                                     self.get_degree(degreeLine.text()), self.mainWindow.objList.currentItem()))

        layout.addWidget(QLabel('Opções de Rotação'))
        layout.addWidget(originButton)
        layout.addWidget(pointButton)
        layout.addWidget(objCenterButton)
        layout.addWidget(QLabel('Ângulo de Rotação'))
        layout.addWidget(degreeLine)
        layout.addWidget(addButton)

        return(layout)
        
    def add_escalonamento(self) -> QFormLayout:
        layout = QFormLayout()

        originButton = QRadioButton('Escalonar sobre a origem')
        pointButton = QRadioButton('Escalonar sobre o ponto')
        objCenterButton = QRadioButton('Escalonar sobre o centro do objeto')
        addButton = QPushButton("Adicionar")
        degreeLine = QLineEdit()

        # axis = self.get_axis(originButton, pointButton, objCenterButton)
        # #degree = float(degreeLine.text())
        # degree = self.get_degree(degreeLine.text())
        # object = self.mainWindow.objList.currentItem()

        addButton.clicked.connect(lambda: self.add_transform(3,self.get_axis(originButton, pointButton, objCenterButton),\
                                     self.get_degree(degreeLine.text()), self.mainWindow.objList.currentItem()))

        layout.addWidget(QLabel('Opções de escalonamento'))
        layout.addWidget(originButton)
        layout.addWidget(pointButton)
        layout.addWidget(objCenterButton)
        layout.addWidget(QLabel('Ângulo de Escalonamento'))
        layout.addWidget(degreeLine)
        layout.addWidget(addButton)

        return(layout)

    def confirm_button(self):
        self.transformation_control.confirm_button()

    def add_transform(self, type: int, axis: int, degree: float, object: Form):
        self.transformation_control.add_transform(type, axis, degree, object)

    def get_degree(self, text: str) -> float:
        if text != "":
            return float(text)
        return 1 #TODO

    def get_axis(self, originButton: QRadioButton, pointButton: QRadioButton, objCenterButton: QRadioButton) -> int:
        if originButton.isChecked():
            return 1
        elif pointButton.isChecked():
            return 2
        elif objCenterButton.isChecked():
            return 3
        return 0

    

        

