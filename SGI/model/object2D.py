from typing import List, Tuple
from model.form import Form
import numpy as np
t_coordinate = Tuple[float, float]

class Object2D(Form):
    def __init__(self, name: str, coordinates: List[t_coordinate], id: int) -> None:
        self.name = name
        self.coordinates = coordinates
        self.id = id
        self.matrix = self.getMatrix()
        self.normalized = self.coordinates.copy()
        self.color = [0,0,0]
        self.fill = False

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

    def tridimentional(self):
        return False

    def set_visible(self, visible):
        self.visible = visible

    def setCoordinates(self, coordinates: List[t_coordinate]):
        self.coordinates = coordinates

    def setMatrix(self, matrix: []):
        self.matrix = matrix

    def getMatrix(self) -> []:
        coordinates = self.coordinates
        matrix = []
        for coordinate in coordinates:
            x, y = coordinate[0], coordinate[1]
            matrix.append([x,y,1])
        return matrix

    def get_lines(self):
        object_lines = []
        stack = []
        points = self.normalized
        for p in points:
            if len(stack) == 0:
                stack.append(p)
                continue
            p1 = stack.pop()
            p2 = p
            object_lines.append((p1,p2))
            stack.append(p2)
        p2 = points[0]
        p1 = points[len(points)-1]
        object_lines.append((p1,p2))
        return object_lines

    def add_cord(self, coordinate: t_coordinate):
        self.coordinates.append(coordinate)
        self.matrix = self.getMatrix()

    def get_center(self) -> t_coordinate:
        coordinates = self.coordinates
        x, y = (0,0)
        for coordinate in coordinates:
            x = x + coordinate[0]
            y = y + coordinate[1]
        x = x/self.len()
        y = y/self.len()
        return (x,y)

    def len(self)->int:
        return len(self.coordinates)

    def tridimentional(self) -> bool:
        return len(self.coordinates[0]) == 3

    def reform(self):
        matrix = self.matrix
        self.coordinates.clear()
        for line in matrix:
            x, y = line[0], line[1]
            self.coordinates.append([x,y])
