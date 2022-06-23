from typing import List, Tuple
from model.form import Form
from utils import curve
import numpy as np
t_coordinate = Tuple[float, float, float]

class Object3D(Form):
    def __init__(self, name: str, coordinates: List[t_coordinate], id: int) -> None:
        self.name = name
        self.coordinates = coordinates
        self.id = id
        self.matrix = self.getMatrix()
        self.normalized = self.coordinates.copy()
        self.color = [0,0,0]
        self.fill = False
        self.curve_type = 0
        self.is_curvy = False

    def set_color(self, color, format):
        if format:
            self.color = color
        else:
            color = color.lstrip('#')
            lv = len(color)
            rgb = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            self.color = rgb

    def set_fill(self, fill):
        self.fill = fill

    def set_curvy(self, curvy):
        self.is_curvy = curvy

    def set_curve_type(self, curve_type):
        self.curve_type = curve_type

    def tridimentional(self):
        return True

    def set_visible(self, visible):
        self.visible = visible

    def setCoordinates(self, coordinates: List[t_coordinate]):
        self.coordinates = coordinates

    def setMatrix(self, matrix: []):
        self.matrix = matrix

    def set_edges(self, edges: []):
        self.edges = edges

    def getMatrix(self) -> []:
        coordinates = self.coordinates
        matrix = []
        for coordinate in coordinates:
            x, y, z = coordinate[0], coordinate[1], coordinate[2]
            matrix.append([x,y,z,1]) #ISSO PODE ESTAR ERRADO
        return matrix

    def get_lines(self):
        if self.is_curvy:
            return self.curve()
        object_lines = []
        stack = []
        points = self.normalized
        for p in self.edges:
            object_lines.append((points[p[0]-1], points[p[1]-1]))
        return object_lines

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

    def tridimentional(self) -> bool:
        return len(self.coordinates[0]) == 3

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
