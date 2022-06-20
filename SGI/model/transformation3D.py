from model.form import Form
from model.transformation import Transformation
from typing import Tuple, List
from utils import matrices
import numpy as np
import math

t_coordinate = Tuple[float, float, float]

class Transformation3D(Transformation):

    def __init__(self, type: int, degree: float, point: t_coordinate, vector: t_coordinate, rotate_around_axis: int, rotate_by_axis: int, object: Form, id: int) -> None:
        self.type = type
        self.degree = degree
        self.point = point
        self.vector = vector
        self.rotate_around_axis = rotate_around_axis
        self.rotate_by_axis = rotate_by_axis
        self.object = object
        self.id = id
        self.create_matrix()

    def create_matrix(self):
        print("rotate_around_axis: "+str(self.rotate_around_axis))
        print("rotate_by_axis: "+str(self.rotate_by_axis))
        if self.type == 1:
            self.translation()
        elif self.type == 2:
            self.rotation()
        elif self.type == 3:
            self.scaling()
        elif self.type == 4:
            self.window_rotation()

    def set_axis(axis):
        self.axis = axis

    def translation(self):
        x, y, z = self.point[0], self.point[1], self.point[2]
        self.matrix = matrices.translation((x,y,z),matrices.identity())

    def rotation(self):
        vector, point = self.vector, self.point
        if self.rotate_around_axis == 1:
            point = (0,0,0)
        elif self.rotate_around_axis == 2:
            pass
        elif self.rotate_around_axis == 3:
            point = self.object.get_center()
        if self.rotate_by_axis == 1:
            vector = (1,0,0)
        elif self.rotate_by_axis == 2:
            vector = (0,1,0)
        elif self.rotate_by_axis == 3:
            vector = (0,0,1)
        print("vector: "+str(vector))
        print("point: "+str(point))
        self.rotate(vector, point)


    def rotate(self, vector, point):
        x, y, z = point[0], point[1], point[2]
        v1, v2 = (0,0,0), (vector[0], vector[1], vector[2])
        matrix = matrices.identity()
        #1 Transladar para a Origem
        matrix1 = matrices.translation((-x,-y,-z),matrix)
        #2 Rotacionar sobre o eixo-x
        p1, p2, p3 = v1, (0, v2[1], v2[2]), (0, v2[1], 0)
        theta_x = matrices.degree(p1,p2,p3) #SIGN
        matrix2 = matrices.rotation_x(theta_x, matrix1)
        #3 Rotacionar sobre o eixo-z
        m = matrices.rotation_x(theta_x,[v2[0],v2[1],v2[2],1])
        v2 = (m[0],m[1],m[2])
        p1, p2, p3 = v1, v2, (0, v2[1], 0)
        theta_z = matrices.degree(p1,p2,p3)
        matrix3 = matrices.rotation_z(theta_z, matrix2)
        #4 Rotacionar sobre o eixo-y
        theta = self.degree
        matrix4 = matrices.rotation_y(theta, matrix3)
        #5 Desfazer Rotação sobre o eixo-z
        matrix5 = matrices.rotation_z(-theta_z, matrix4)
        #6 Desfazer Rotação sobre o eixo-x
        matrix6 = matrices.rotation_x(-theta_x, matrix5)
        #7 Desfazer Translação
        matrix7 = matrices.translation((x,y,z), matrix6)
        self.matrix = matrix7

    def rotation_vector(self, vector):
        x, y, z = self.object.get_center()
        v1, v2 = (0,0,0), (vector[0], vector[1], vector[2])
        matrix = matrices.identity()
        #1 Transladar para a Origem
        matrix1 = matrices.translation((-x,-y,-z),matrix)
        #2 Rotacionar sobre o eixo-x
        p1, p2, p3 = v1, (0, v2[1], v2[2]), (0, v2[1], 0)
        theta_x = -matrices.degree(p1,p2,p3)
        matrix2 = matrices.rotation_x(theta_x, matrix1)
        #3 Rotacionar sobre o eixo-z
        m = matrices.rotation_x(theta_x,[v2[0],v2[1],v2[2],1])
        v2 = (m[0],m[1],m[2])
        p1, p2, p3 = v1, v2, (0, v2[1], 0)
        theta_z = matrices.degree(p1,p2,p3)
        matrix3 = matrices.rotation_z(theta_z, matrix2)
        #4 Rotacionar sobre o eixo-y
        theta = self.degree
        matrix4 = matrices.rotation_y(theta, matrix3)
        #5 Desfazer Rotação sobre o eixo-z
        matrix5 = matrices.rotation_z(-theta_z, matrix4)
        #6 Desfazer Rotação sobre o eixo-x
        matrix6 = matrices.rotation_x(-theta_x, matrix5)
        #7 Desfazer Translação
        matrix7 = matrices.translation((x,y,z), matrix6)
        self.matrix = matrix7

    def rotation_axis(self, point: t_coordinate):
        axis = self.rotate_by_axis
        x, y, z = -point[0], -point[1], -point[2]
        matrix = matrices.identity()
        matrix = matrices.translation((x,y,z),matrix)
        if axis == 1:
            theta_x = self.degree
            matrix = matrices.rotation_x(theta_x, matrix)
        elif axis == 2:
            theta_y = self.degree
            matrix = matrices.rotation_y(theta_y, matrix)
        elif axis == 3:
            theta_z = self.degree
            matrix = matrices.rotation_z(theta_z, matrix)
        matrix = matrices.translation((-x,-y,-z), matrix)
        self.matrix = matrix


    def scaling(self):
        scale = self.point
        matrix = matrices.identity()
        center = self.object.get_center()
        self.matrix = matrices.scaling(scale, center, matrix)

    def window_rotation(self):
        theta = self.degree
        x, y, z = self.point
        matrix = matrices.identity()
        matrix = matrices.translation((-x,-y,-z), matrix)
        matrix = matrices.rotation_z(theta, matrix)
        matrix = matrices.translation((x,y,z), matrix)
        self.matrix = matrix


    def apply(self):
        self.object.setMatrix(np.dot(self.object.matrix, self.matrix))
        #self.object.setMatrix(self.matrix)
        self.object.reform()

    def normalize(self):
        matrix = np.dot(self.object.matrix, self.matrix)
        self.object.normalized.clear()
        for line in matrix:
            x, y, z = line[0], line[1], line[2]
            self.object.normalized.append([x,y,z])
        self.object.show()

    def degree(self, p1, p2, p3):
        hipo = self.dist(p1,p2)
        cat_op = self.dist(p2,p3)
        cat_ad = self.dist(p1, p3)
        sign, x, y = 1, p3[0], p3[1]
        sin = cat_op/hipo
        cos = cat_ad/hipo
        quad = 0
        degree = np.degrees(np.arcsin(sin))
        if x < 0:
            if y < 0: #3rd
                degree = 180 - degree
            else:     #2nd
                degree += 180
        else:
            if y < 0: #4th
                degree += 360
            else:     #1st
                pass
        return degree

    def dist(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
