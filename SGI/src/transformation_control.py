from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, QDialogButtonBox

from typing import List
from form import Form
from viewport import Viewport
from transformation import Transformation
# from gui import MainWindow

class Transformation_control(QDialog):
    def __init__(self, viewport: Viewport, transformation_gui) -> None:
        super().__init__()
        # self.add_object_window()
        self.viewport = viewport
        self.transformation_gui = transformation_gui
        self.transList: List[Transformation] = list()

    def confirm_button(self):
        for transformation in self.transList:
            transformation.transform()
        self.transList.clear()
        self.transformation_gui.transformList.clear()


    def add_transform(self, type: int, axis: int, degree: float, object: Form):
        transformation = Transformation(type, axis, degree, object , len(self.transList))
        self.transList.append(transformation)
        print(object.id)
        self.transformation_gui.transformList.addItem(str(transformation.id))
        

