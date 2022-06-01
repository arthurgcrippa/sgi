from typing import List, Tuple
import numpy as np
t_coordinate = Tuple[float, float]

class Form():
    def __init__(self, name: str, coordinates: List[t_coordinate], id: int) -> None:
        self.name = name
        self.coordinates = coordinates
        self.id = id
        self.matrix = self.getMatrix()
        self.normalized = self.coordinates.copy()
        self.color = [0,0,0]
        self.fill = False
        self.curve_type = 0
        self.steps = 1000
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

    def set_visible(self, visible):
        self.visible = visible

    def add_cord(self, coordinate: t_coordinate):
        self.coordinates.append(coordinate)
        self.matrix = self.getMatrix()

    def len(self)->int:
        return len(self.coordinates)

    def get_center(self) -> t_coordinate:
        coordinates = self.coordinates
        x, y = (0,0)
        for coordinate in coordinates:
            x = x + coordinate[0]
            y = y + coordinate[1]
        x = x/self.len()
        y = y/self.len()
        return (x,y)

    def get_lines(self):
        if self.is_curvy:
            return self.curve()
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

    # transformada de viewport
    def vp_trans(self, wCoord: t_coordinate, wMin: t_coordinate, wMax: t_coordinate, vpCoordinate: t_coordinate) -> t_coordinate:
        vp_x = ((wCoord[0] - wMin[0])/(wMax[0]-wMin[0]))*vpCoordinate[0]
        vp_y = (1-((wCoord[1]-wMin[1])/(wMax[1]-wMin[1])))*vpCoordinate[1]
        return (int(vp_x), int(vp_y))

    def setCoordinates(self, coordinates: List[t_coordinate]):
        self.coordinates = coordinates

    def getMatrix(self) -> []:
        coordinates = self.coordinates
        matrix = []
        for coordinate in coordinates:
            x, y = coordinate[0], coordinate[1]
            matrix.append([x,y,1])
        return matrix

    def setMatrix(self, matrix: []):
        self.matrix = matrix

    def reform(self):
        matrix = self.matrix
        self.coordinates.clear()
        for line in matrix:
            x, y = line[0], line[1]
            self.coordinates.append([x,y])

    def curve(self):
        lines = []
        if (self.len()-1) % 3 != 0:
            print("Problemas! Não há como formar p1, p2, ")
            print(self.len())
        else:
            p1 = self.normalized[0]
            for i in range(1, self.len()):
                if i % 3 == 0:
                    p2 = self.normalized[i]
                    partial_lines = self.partial_curve(p1,p2,r1,r2)
                    p1 = p2
                    for line in partial_lines:
                        lines.append(line)
                if i % 3 == 1:
                    r1 = self.normalized[i]
                if i % 3 == 2:
                    r2 = self.normalized[i]
        return lines

    def partial_curve(self, p1: t_coordinate, p4: t_coordinate, r1: t_coordinate, r4: t_coordinate):
        lines = []
        x1, y1 = p1[0], p1[1]
        for i in range(0, self.steps+1):
            t = i/self.steps
            x2, y2 = x1, y1
            if self.curve_type:
                x2, y2 = self.hermite(p1, r1, r4, p4, t)
            else:
                x2, y2 = self.bezier(p1, r1, r4, p4, t)
            lines.append(((x1,y1), (x2,y2)))
            x1, y1 = x2, y2
        return lines

    def bezier(self, p0, p1, p2, p3, t):
        s = 1-t
        x = s**3 * p0[0] + 3 * s**2 * t * p1[0] + 3 * s * t**2 * p2[0] + t**3 * p3[0]
        y = s**3 * p0[1] + 3 * s**2 * t * p1[1] + 3 * s * t**2 * p2[1] + t**3 * p3[1]
        return x, y

    def hermite(self, p1, r1, r4, p4, t):
        x = p1[0] * (2*t**3 - 3*t**2 + 1) + p4[0] * (-2*t**3 + 3*t**2) + r1[0] * (t**3 - 2*t**2 + t) + r4[0] * (t**3 - t**2)
        y = p1[1] * (2*t**3 - 3*t**2 + 1) + p4[1] * (-2*t**3 + 3*t**2) + r1[1] * (t**3 - 2*t**2 + t) + r4[1] * (t**3 - t**2)
        return x, y
