from model.form import Form
from model.viewport import Viewport
from typing import Tuple, List
import numpy as np
import math

t_coordinate = Tuple[float, float]

class Transformation():

    def __init__(self, type: int, degree: float, point: t_coordinate, object: Form, id: int) -> None:
        self.type = type
        self.degree = degree
        self.point = point
        self.object = object
        self.id = id
        self.create_matrix()

    def create_matrix(self):
        if self.type == 1:
            self.translation()
        elif self.type == 2:
            self.rotation()
        elif self.type == 3:
            self.scaling()

    def translation(self):
        x, y = self.point[0], self.point[1]
        self.matrix = [[1,0,0],
                       [0,1,0],
                       [x,y,1]]

    def rotation(self):
        tetha = math.radians(self.degree)
        sin, cos = np.sin(tetha), np.cos(tetha)
        x, y = self.point[0], self.point[1]
        matrix_rotation = [[cos,-1*sin, 0],
                           [sin,   cos, 0],
                           [ 0,     0,  1]]

        matrix_translation = [[   1,    0, 0],
                              [   0,    1, 0],
                              [-1*x, -1*y, 1]]

        matrix_reverse_translation = [[1,0,0],
                                      [0,1,0],
                                      [x,y,1]]

        self.matrix = np.dot(np.dot(matrix_translation, matrix_rotation), matrix_reverse_translation)

    def scaling(self):
        dx, dy = self.point[0], self.point[1]
        x, y = self.object.get_center()

        matrix_scaling = [[dy,0,0],
                          [0,dy,0],
                          [0,0,1]]

        matrix_translation = [[   1,    0, 0],
                              [   0,    1, 0],
                              [-1*x, -1*y, 1]]

        matrix_reverse_translation = [[1,0,0],
                                      [0,1,0],
                                      [x,y,1]]

        self.matrix = np.dot(np.dot(matrix_translation, matrix_scaling), matrix_reverse_translation)

    def apply(self):
        self.object.setMatrix(np.dot(self.object.matrix, self.matrix))
        self.object.reform()
