from typing import List, Tuple
from model.form import Form
from utils import curve
import numpy as np
t_coordinate = Tuple[float, float, float]

class Object3D(Form):
    def __init__(self, name: str, coordinates: List[t_coordinate], id: int) -> None:
        #Basic Attriutes
        self.name = name
        self.coordinates = coordinates
        self.color = [0,0,0]
        self.id = id

        #Normalization Attriutes
        self.matrix = self.getMatrix()
        self.normalized = self.coordinates.copy()

        #Flags
        self.IS_POLYGON = False
        self.curve_type = 0 #bspline, hermite or bezier
        self.IS_CURVE = False
        self.IS_GROUPED = False


    def set_color(self, color, format):
        if format:
            self.color = color
        else:
            color = color.lstrip('#')
            lv = len(color)
            rgb = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            self.color = rgb

    def set_as_polygon(self, FLAG):
        self.IS_POLYGON = FLAG

    def set_as_curve(self, FLAG):
        self.IS_CURVE = FLAG

    def set_curve_type(self, curve_type):
        self.curve_type = curve_type

    def setCoordinates(self, coordinates: List[t_coordinate]):
        self.coordinates = coordinates

    def setMatrix(self, matrix: []):
        self.matrix = matrix

    def set_edges(self, edges: []):
        self.edges = edges
        if len(edges) in [1,2]:
            self.IS_GROUPED = False
            return
        _, last_flag = edges[0]
        for _,flag in edges:
            if flag != last_flag:
                self.IS_GROUPED = True
                return
        self.IS_GROUPED = False

    def tridimentional(self):
        return True

    def grouped(self):
        return self.IS_GROUPED

    def getMatrix(self) -> []:
        coordinates = self.coordinates
        matrix = []
        for coordinate in coordinates:
            x, y, z = coordinate[0], coordinate[1], coordinate[2]
            matrix.append([x,y,z,1])
        return matrix

    def get_lines(self):
        if self.IS_CURVE:
            return self.curve()
        object_lines = []
        points = self.normalized
        for [circuit, _] in self.edges:
            for i in range(0, len(circuit)-1):
                object_lines.append((points[circuit[i]-1], points[circuit[i+1]-1]))
        return object_lines

    def get_group_lines(self):
        group = []
        points = self.normalized
        for (circuit, flag) in self.edges:
            component = []
            for i in range(0, len(circuit)-1):
                component.append((points[circuit[i]], points[circuit[i+1]]))
            group.append((component, flag))
        return group


    def add_cord(self, coordinate: t_coordinate):
        self.coordinates.append(coordinate)
        self.matrix = self.getMatrix()

    def get_center(self) -> t_coordinate:
        coordinates = self.coordinates
        x, y, z = (0,0,0)
        for coordinate in coordinates:
            x = x + coordinate[0]
            y = y + coordinate[1]
            z = z + coordinate[2]
        x = x/self.len()
        y = y/self.len()
        z = z/self.len()
        return (x,y,z)

    def len(self)->int:
        return len(self.coordinates)

    def reform(self):
        matrix = self.matrix
        self.coordinates.clear()
        for line in matrix:
            x, y, z = line[0], line[1], line[2]
            self.coordinates.append([x,y,z])

    def curve(self):
        lines = []
        if self.curve_type:
            lines = curve.blending_curve(self.normalized, self.curve_type)
        else:
            lines = curve.b_spline_curve(self.normalized, self.curve_type)
        return lines

    def show(self):
        id = 1
        for coordinate in self.normalized:
            print("p"+str(id)+" : "+str(coordinate))
            id += 1
        print("#########################")
