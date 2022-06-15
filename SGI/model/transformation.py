from model.form import Form
from typing import Tuple, List
import numpy as np
import math

t_coordinate = Tuple[float, float, float]

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
        elif self.type == 4:
            self.window_rotation()

    def translation(self):
        x, y, z = self.point[0], self.point[1], self.point[2]
        self.matrix = [[1,0,0,0],
                       [0,1,0,0],
                       [0,0,1,0],
                       [x,y,z,1]]

    def rotation(self):
        p1, p2 = (0,0,0), self.point
        x, y, z = self.object.get_center()
        p2 = (p2[0]-x, p2[1]-y, p2[2]-z)

        #1 Transladar para a origem
        matrix_translation = [[1,0,0,0],
                              [0,1,0,0],
                              [0,0,1,0],
                              [-x,-y,-z,1]]

        #2 Rotacionar sobre o eixo-x
        p3 = (p2[0], p2[1], 0)
        sin, cos = self.trigonometry(p1,p2,p3)
        sin_x, cos_x = sin,cos
        matrix_rotation_x = [[1,   0,    0,    0],
                             [0,  cos,  sin,   0],
                             [0, -sin,  cos,   0],
                             [0,   0,    0,    1]]

        #3 Rotacionar sobre o eixo-z
        p3 = (0, p2[1], p2[2])
        sin, cos = self.trigonometry(p1,p2,p3)
        sin_z, cos_z = sin,cos
        matrix_rotation_z = [[cos, sin,   0,  0],
                             [-sin, cos,  0,  0],
                             [0,     0,   1,  0],
                             [0,     0,   0,  1]]

        #4 Rotacionar sobre o eixo-y em tetha
        tetha = math.radians(self.degree)
        sin, cos = np.sin(tetha), np.cos(tetha)
        matrix_rotation_y = [[cos, 0, -sin, 0],
                             [0,   1,   0,  0],
                             [sin, 0,  cos,  0],
                             [0,   0,   0,  1]]

        #4 Desfazer rotação sobre o eixo-z
        sin, cos = -sin_z, -cos_z
        matrix_reverse_rotation_z = [[cos, sin,   0,  0],
                                     [-sin, cos,  0,  0],
                                     [0,     0,   1,  0],
                                     [0,     0,   0,  1]]

        #5 Desfazer rotação sobre o eixo-x
        sin, cos = -sin_x, -cos_x
        matrix_reverse_rotation_x = [[1,   0,    0,    0],
                                     [0,  cos,  sin,   0],
                                     [0, -sin,  cos,   0],
                                     [0,   0,    0,    1]]

        #Desfazer a translação
        matrix_reverse_translation = [[1,0,0,0],
                                      [0,1,0,0],
                                      [0,0,1,0],
                                      [x,y,z,1]]
        self.matrix = np.dot(np.dot(np.dot(np.dot(np.dot(np.dot(matrix_translation, matrix_rotation_x),matrix_rotation_z),matrix_rotation_y),matrix_reverse_rotation_z),matrix_reverse_rotation_x),matrix_reverse_translation)

    def scaling(self):
        dx, dy, dz = self.point[0], self.point[1], self.point[2]
        x, y, z = self.object.get_center()

        matrix_scaling = [[dy,0,0,0],
                          [0,dy,0,0],
                          [0,0,dz,0],
                          [0,0,0,1]]

        matrix_translation = [[1,   0,  0, 0],
                              [0,   1,  0, 0],
                              [0,   0,  1, 0],
                              [-x, -y, -z, 1]]

        matrix_reverse_translation = [[1,0,0,0],
                                      [0,1,0,0],
                                      [0,0,1,0],
                                      [x,y,z,1]]

        self.matrix = np.dot(np.dot(matrix_translation, matrix_scaling), matrix_reverse_translation)


    def window_rotation(self):

        tetha = math.radians(self.degree)
        sin, cos = np.sin(tetha), np.cos(tetha)
        x, y, z = self.point

        matrix_window_rotation = [[cos, sin,   0,  0],
                                  [-sin, cos,  0,  0],
                                  [0,     0,   1,  0],
                                  [0,     0,   0,  1]]

        matrix_translation = [[1,   0,  0, 0],
                              [0,   1,  0, 0],
                              [0,   0,  1, 0],
                              [-x, -y, -z, 1]]

        matrix_reverse_translation = [[1,0,0,0],
                                      [0,1,0,0],
                                      [0,0,1,0],
                                      [x,y,z,1]]

        self.matrix = np.dot(np.dot(matrix_window_rotation, matrix_translation), matrix_reverse_translation)


    def apply(self):
        #print("Matrix Resultado: "+str(np.dot(self.object.matrix, self.matrix)))
        self.object.setMatrix(np.dot(self.object.matrix, self.matrix))
        self.object.reform()

    def normalize(self):
        matrix = np.dot(self.object.matrix, self.matrix)
        self.object.normalized.clear()
        for line in matrix:
            x, y, z = line[0], line[1], line[2]
            self.object.normalized.append([x,y,z])

    def trigonometry(self, p1, p2, p3):
        hipo = self.dist(p1,p2)
        cat_op = self.dist(p2,p3)
        cat_ad = self.dist(p1, p3)
        sin = cat_op/hipo
        cos = cat_ad/hipo
        return sin, cos

    def dist(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
