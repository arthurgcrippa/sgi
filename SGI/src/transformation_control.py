from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, QDialogButtonBox

from typing import List
from form import Form
from viewport import Viewport
from transformation import Transformation
from typing import Tuple

t_coordinate = Tuple[float, float]
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


    def add_transform_rotation(self, type: int, axis: int, degree: float, object: Form, point: t_coordinate):
        transformation = Transformation(type, axis, degree, object, len(self.transList), point)
        self.transList.append(transformation)
        print(object.id)
        self.transformation_gui.transformList.addItem(str(transformation.id))

    # def add_transform_translaction(self, type: int, point_diff: t_coordinate, object: Form):
    #     transformation = Transformation(type, point_diff, object , len(self.transList))
    #     self.transList.append(transformation)
    #     print(object.id)
    #     self.transformation_gui.transformList.addItem(str(transformation.id))

    # def add_transform_escaling(self, type: int, escale: int, object: Form):
    #     transformation = Transformation(type, escale, object , len(self.transList))
    #     self.transList.append(transformation)
    #     print(object.id)
    #     self.transformation_gui.transformList.addItem(str(transformation.id))


