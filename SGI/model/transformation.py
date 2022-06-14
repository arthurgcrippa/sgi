from model.form import Form
from typing import Tuple, List
import numpy as np
import math

t_coordinate = Tuple[float, float, float]

class Transformation():

    def __init__(self, type: int, degree: float, point: t_coordinate, vector: List[t_coordinate], object: Form, id: int) -> None:
        self.type = type
        self.degree = degree
        self.point = point
        self.vector = vector
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
        x, y, z = self.point[0], self.point[1], self.point[2]
        self.matrix = [[1,0,0,0],
                       [0,1,0,0],
                       [0,0,1,0],
                       [x,y,z,1]]

    def rotation(self):
        p1, p2 = self.vector[0], self.vector[1]
        x, y, z = p1[0] + p2[0], p1[1] + p2[1], p1[2] + p2[2]
        x, y, z = x/2, y/2, z/2

        #1 Translação pro Eixo
        matrix_translation = [[1,0,0,0],
                              [0,1,0,0],
                              [0,0,1,0],
                              [-x,-y,-z,1]]

        #2 Rotação em X e Y
        hipo = math.sqrt((p2[0]-x)**2 + (p2[1]-y)**2 + (p2[2]-z)**2)
        cat_op = math.sqrt(p2[1]**2 + p2[2]**2)
        cat_ad = math.sqrt((p2[0]-x)**2 + y**2 + z**2)

        sin = cat_op/hipo
        cos = cat_ad/hipo
        sin_xz, cos_xz = sin,cos


        matrix_rotation_x = [[1,   0,    0,    0],
                             [0,  cos,  sin,   0],
                             [0, -sin,  cos,   0],
                             [0,   0,    0,    1]]

        matrix_rotation_z = [[cos, sin,   0,  0],
                             [-sin, cos,  0,  0],
                             [0,     0,   1,  0],
                             [0,     0,   0,  1]]

        #3 Rotacionar sobre Y em tetha

        tetha = math.radians(self.degree)
        sin, cos = np.sin(tetha), np.cos(tetha)

        matrix_rotation_y = [[cos, 0, -sin, 0],
                             [0,   1,   0,  0],
                             [sin, 0,  cos,  0],
                             [0,   0,   0,  1]]

        #4 Desrotacionar sore X e Z
        sin, cos = -sin_xz, -cos_xz
        matrix_reverse_rotation_x = [[1,   0,    0,    0],
                                     [0,  cos,  sin,   0],
                                     [0, -sin,  cos,   0],
                                     [0,   0,    0,    1]]

        matrix_reverse_rotation_z = [[cos, sin,   0,  0],
                                     [-sin, cos,  0,  0],
                                     [0,     0,   1,  0],
                                     [0,     0,   0,  1]]



        #Desfaz a Translação
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


    def apply(self):
        print("Matrix Resultado: "+str(np.dot(self.object.matrix, self.matrix)))
        self.object.setMatrix(np.dot(self.object.matrix, self.matrix))
        self.object.reform()

    def normalize(self):
        matrix = np.dot(self.object.matrix, self.matrix)
        self.object.normalized.clear()
        for line in matrix:
            x, y, z = line[0], line[1], line[2]
            self.object.normalized.append([x,y,z])
