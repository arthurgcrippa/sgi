from gettext import translation
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, QDialogButtonBox

from typing import List, Tuple
from model.form import Form
from model.viewport import Viewport
from model.transformation import Transformation

t_coordinate = Tuple[float, float]

class Transformation_control(QDialog):
    def __init__(self, viewport: Viewport, transformation_gui) -> None:
        super().__init__()
        # self.add_object_window()
        self.viewport = viewport
        self.transformation_gui = transformation_gui
        self.transList: List[Transformation] = list()

    def confirm_button(self):

        for transformation in self.transList:
            transformation.apply()
        self.viewport.redraw()
        self.transList.clear()
        self.transformation_gui.transformList.clear()

    def add_translaction(self, type: int, point: t_coordinate, object: Form):
        transformation = Transformation(type, None, point, object, len(self.transList))
        self.transList.append(transformation)
        self.transformation_gui.transformList.addItem("Translada Objeto: " + str(object.id))

    def add_rotation(self, type: int, degree: float, point: t_coordinate, object: Form):
        transformation = Transformation(type, degree, point, object, len(self.transList))
        self.transList.append(transformation)
        self.transformation_gui.transformList.addItem("Rotaciona Objeto: " + str(object.id) + " em %.1f graus"%degree)

    def add_scaling(self, type: int, point: t_coordinate, object: Form):
        transformation = Transformation(type, None, point, object, len(self.transList))
        self.transList.append(transformation)
        self.transformation_gui.transformList.addItem("Altera Magnitude do Objeto: "+ str(object.id))
