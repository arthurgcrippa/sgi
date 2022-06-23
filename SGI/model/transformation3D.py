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
        if self.type == 1:
            self.translation()
        elif self.type == 2:
            self.rotation()
        elif self.type == 3:
            self.scaling()
        elif self.type == 4:
            self.projection()

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
        self.rotate(vector, point)


    def rotate(self, vector, point):
        x, y, z = point[0], point[1], point[2]
        v1, v2 = (0,0,0), (vector[0], vector[1], vector[2])
        matrix = matrices.identity()
        #1 Transladar para a Origem
        matrix1 = matrices.translation((-x,-y,-z),matrix)
        #2 Rotacionar sobre o eixo-x
        p1, p2, p3 = v1, (0, v2[1], v2[2]), (0, v2[1], 0)
        theta_x = -matrices.degree(p1,p2,p3) #SIGN
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


    def scaling(self):
        scale = self.point
        matrix = matrices.identity()
        center = self.object.get_center()
        self.matrix = matrices.scaling(scale, center, matrix)

    def projection(self):
        matrix = matrices.identity()
        self.matrix = matrices.project(-100, matrix)

    def apply(self):
        self.object.setMatrix(np.dot(self.object.matrix, self.matrix))
        #self.object.setMatrix(self.matrix)
        self.object.reform()

    def normalize(self, object_matrix):
        print("Object Matrix:")
        matrices.show(object_matrix[0])
        print("Transformation Matrix: ")
        matrices.show(self.matrix)
        matrix = np.dot(object_matrix[0], self.matrix)
        print("Result Matrix:")
        matrices.show(matrix)
        self.object.normalized.clear()
        for line in matrix:
            x, y, z, w = line[0], line[1], line[2], line[3]
            #print("xyzw before")
            before = (x,y,z,w)
            #print(before)
            if w != 0:
        #        print("w: "+str(w))
                x, y, z = x/w, y/w, z/w
                #print("xyzw after")
                after = (x,y,z,w)
                #print(after)
            self.object.normalized.append([x,y,z])
        object_matrix.clear()
        object_matrix.append(matrix)

    def dist(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
