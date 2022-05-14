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
        # print(object.id)
        self.transformation_gui.transformList.addItem("Rotaciona Objeto: " + str(object.id) + " em "+ str(degree) +" graus")

    def add_scaling(self, type: int, point: t_coordinate, object: Form):
        transformation = Transformation(type, None, point, object, len(self.transList))
        self.transList.append(transformation)
        # print(object.id)
        self.transformation_gui.transformList.addItem("Altera Magnitude do Objeto: "+str(object.id))       


    def rotate_window(self, degrees: int, orientation: int):
        if not(orientation):
            degrees = degrees * -1
        self.window.theta += degrees
        self.viewport.redraw()

    def update_normal_coord(self, form: Form) -> None:
        degree = self.window.theta

        x_cw = (self.window.xMax - self.window.xMin) / 2
        y_cw = (self.window.yMax - self.window.yMin) / 2

        window_center = [x_cw, y_cw]

        window_translaction = Transformation(1, degree, window_center, None, None)

        # op_mtx = self.__translation_mtx(-self.window.center[0], -self.window.center[-1])
        # op_mtx = op_mtx @ self.__rotation_mtx(-degrees)
        # op_mtx = op_mtx @ self.__scale_mtx(1/w_dx, 1/w_dy)

        # res_mtx = obj.homogenous_coordinates() @ op_mtx

        # obj.update_normal_coord(res_mtx)