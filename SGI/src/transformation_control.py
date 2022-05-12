from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QListWidget, QLayout, QGridLayout, QToolButton, QDialog, QTabWidget, QFormLayout, QLineEdit,QCheckBox, QDialogButtonBox

from typing import List, Tuple
from form import Form
from viewport import Viewport
from transformation import Transformation

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
        print(object.id)
        self.transformation_gui.transformList.addItem(str(transformation.id))

    # def add_rotation(self, type: int, axis: int, degree: float, point: t_coordinate, object: Form):
    #     x,y = (0,0)
    #     if axis == 3:
    #         for coordinate in object.coordinates:
    #             x = x + coordinate[0]
    #             y = y + coordinate[1]
    #         x = x/len(object.coordinates)
    #         y = y/len(object.coordinates)
    #         point = (x,y)
    #     point = (-1*point[0], -1*point[1])
    #     for obj in self.viewport.objectList:
    #         self.add_translaction(1, point, obj)       
    #     transformation = Transformation(type, axis, degree, point, object, len(self.transList))
    #     self.transList.append(transformation)
    #     print(object.id)
    #     self.transformation_gui.transformList.addItem(str(transformation.id))
    #     point = (-1*point[0], -1*point[1])
    #     for obj in self.viewport.objectList:
    #         self.add_translaction(1, point, obj)

    def add_rotation(self, type: int, degree: float, point: t_coordinate, object: Form):
        transformation = Transformation(type, degree, point, object, len(self.transList))
        self.transList.append(transformation)
        print(object.id)
        self.transformation_gui.transformList.addItem(str(transformation.id))

    def add_scaling(self, type: int, point: t_coordinate, object: Form):
        transformation = Transformation(type, None, point, object, len(self.transList))
        self.transList.append(transformation)
        print(object.id)
        self.transformation_gui.transformList.addItem(str(transformation.id))       


