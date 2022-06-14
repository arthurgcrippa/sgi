from typing import List, Tuple
import numpy as np
t_coordinate = Tuple[float, float, float]

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
        self.curve_algo = 0
        self.steps = 1000
        self.delta = self.get_delta()
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

    # def get_lines(self):
    #     if self.is_curvy:
    #         return self.curve()
    #     object_lines = []
    #     stack = []
    #     points = self.normalized
    #     for p in points:
    #         if len(stack) == 0:
    #             stack.append(p)
    #             continue
    #         p1 = stack.pop()
    #         p2 = p
    #         object_lines.append((p1,p2))
    #         stack.append(p2)
    #     p2 = points[0]
    #     p1 = points[len(points)-1]
    #     object_lines.append((p1,p2))
    #     return object_lines

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

    # transformada de viewport
    def vp_trans(self, wCoord: t_coordinate, wMin: t_coordinate, wMax: t_coordinate, vpCoordinate: t_coordinate) -> t_coordinate:
        vp_x = ((wCoord[0] - wMin[0])/(wMax[0]-wMin[0]))*vpCoordinate[0]
        vp_y = (1-((wCoord[1]-wMin[1])/(wMax[1]-wMin[1])))*vpCoordinate[1]
        return (int(vp_x), int(vp_y))

    def reform(self):
        matrix = self.matrix
        self.coordinates.clear()
        for line in matrix:
            x, y, z = line[0], line[1], line[2]
            self.coordinates.append([x,y,z])

    def curve(self):
        lines = []
        if self.curve_type:
            lines = self.blending_curve()
        else:
            lines = self.b_spline_curve()
        return lines

    def blending_curve(self):
        lines = []
        if (self.len()-1) % 3 != 0:
            print("Problemas! Não há como formar p1, p2, ")
            print(self.len())
        else:
            p1 = self.normalized[0]
            for i in range(1, self.len()):
                if i % 3 == 0:
                    p2 = self.normalized[i]
                    partial_lines = self.curve_segment(p1,r1,r2,p2)
                    p1 = p2
                    for line in partial_lines:
                        lines.append(line)
                if i % 3 == 1:
                    r1 = self.normalized[i]
                if i % 3 == 2:
                    r2 = self.normalized[i]
        return lines

    def b_spline_curve(self):
        lines = []
        if self.len() < 4:
            print("Problemas! Não há como formar p1, p2, ")
            print(self.len())
        else:
            p0, p1, p2, p3 = self.normalized[0], self.normalized[1], self.normalized[2], self.normalized[3]
            lines = self.curve_segment(p0,p1,p2,p3)
            for i in range(self.len()-4):
                p0 = p1
                p1 = p2
                p2 = p3
                p3 = self.normalized[i+4]
                segment_lines = self.curve_segment(p0, p1, p2, p3)
                for line in segment_lines:
                    #possible line repetition
                    lines.append(line)
        return lines

    def curve_segment(self, p1: t_coordinate, p2: t_coordinate, p3: t_coordinate, p4: t_coordinate):
        lines = []
        if self.curve_algo:
            x1, y1 = self.polynomial_function(p1, p2, p3, p4, 0)
            for i in range(1, self.steps+1):
                t = i/self.steps
                x2, y2 = self.polynomial_function(p1, p2, p3, p4, t)
                lines.append(((x1,y1), (x2,y2)))
                x1, y1 = x2, y2
            return lines
        else:
            return self.forwarding_differences(p1, p2, p3, p4)

    def polynomial_function(self, p1, p2, p3, p4, t):
        t3, t2 = t**3, t**2
        ax, bx, cx, dx = self.polynomial_coeficients(p1[0],p2[0],p3[0],p4[0])
        ay, by, cy, dy = self.polynomial_coeficients(p1[1],p2[1],p3[1],p4[1])
        x = ax*t3 + bx*t2 + cx*t + dx
        y = ay*t2 + by*t2 + cy*t + dy
        return x,y

    def bezier(self, p0, p1, p2, p3, t):
        s = 1-t
        t3, t2 = t**3, t**2
        s3, s2 = s**3, s**2
        x = s3 * p0[0] + 3 * s2 * t * p1[0] + 3 * s * t2 * p2[0] + t3 * p3[0]
        y = s3 * p0[1] + 3 * s2 * t * p1[1] + 3 * s * t2 * p2[1] + t3 * p3[1]
        #x = (1-t)3 * p0[0] + 3 * (1-t)2 * t * p1[0] + 3 * (1-t) * t2 * p2[0] + t3 * p3[0]
        return x, y

    def hermite(self, p1, r1, r4, p4, t):
        t3, t2 = t**3, t**2
        x = p1[0] * (2*t3 - 3*t2 + 1) + p4[0] * (-2*t3 + 3*t2) + r1[0] * (t3 - 2*t2 + t) + r4[0] * (t3 - t2)
        y = p1[1] * (2*t3 - 3*t2 + 1) + p4[1] * (-2*t3 + 3*t2) + r1[1] * (t3 - 2*t2 + t) + r4[1] * (t3 - t2)
        return x, y
        #y = p1[1] * (2*t3 - 3*t2 + 1) + p2[1] * (t3 - 2*t2 + t) + p3[1] * (t3 - t2) + p4[1] * (-2*t3 + 3*t2)

    def b_spline(self, p1, p2, p3, p4, t):
        t2, t3 = t**2, t**3
        x = (-t3+3*t2-3*t+1)*p1[0]/6 + (3*t3 -6*t2 + 4)*p2[0]/6 + (-3*t3 + 3*t2 + 3*t + 1)*p3[0]/6 + (t3)*p4[0]/6
        y = (-t3+3*t2-3*t+1)*p1[1]/6 + (3*t3 -6*t2 + 4)*p2[1]/6 + (-3*t3 + 3*t2 + 3*t + 1)*p3[1]/6 + (t3)*p4[1]/6
        return x, y

    def forwarding_differences(self, p1, p2, p3, p4):

        ax, bx, cx, dx = self.polynomial_coeficients(p1[0], p2[0], p3[0], p4[0])
        ay, by, cy, dy = self.polynomial_coeficients(p1[1], p2[1], p3[1], p4[1])

        _d, _d2, _d3 = self.delta[0], self.delta[1], self.delta[2]

        x, y = dx, dy
        dx, dy = ax*_d3 + bx*_d2 + cx*_d, ay*_d3 + by*_d2 + cy*_d
        d2x, d2y = 6*ax*_d3 + 2*bx*_d2, 6*ay*_d3 + 2*by*_d2
        d3x, d3y = 6*ax*_d3, 6*ay*_d3
        lines = []
        x1 = x
        y1 = y
        for i in range(self.steps):
            x, dx, d2x = x + dx, dx + d2x, d2x + d3x
            y, dy, d2y = y + dy, dy + d2y, d2y + d3y
            x2,y2 = x,y
            lines.append(((x1,y1),(x2,y2)))
            x1, y1 = x2, y2
        return lines

    def polynomial_coeficients(self, v1, v2, v3, v4):
        if self.curve_type == 1:
            a = (+2)*v1+(+1)*v2+(+1)*v3+(-2)*v4
            b = (-3)*v1+(-2)*v2+(-1)*v3+(+3)*v4
            c = (+0)*v1+(+1)*v2+(+0)*v3+(+0)*v4
            d = (+1)*v1+(+0)*v2+(+0)*v3+(+0)*v4
            return a, b, c, d
        elif self.curve_type == 2:
            a = (-1)*v1+(+3)*v2+(-3)*v3+(+1)*v4
            b = (+3)*v1+(-6)*v2+(+3)*v3+(+0)*v4
            c = (-3)*v1+(+3)*v2+(+0)*v3+(+0)*v4
            d = (+1)*v1+(+0)*v2+(+0)*v3+(+0)*v4
            return a, b, c, d
        else:
            a = (-1/6)*v1+(+3/6)*v2+(-3/6)*v3+(+1/6)*v4
            b = (+3/6)*v1+(-6/6)*v2+(+3/6)*v3+(0/6)*v4
            c = (-3/6)*v1+(+0/6)*v2+(+3/6)*v3+(0/6)*v4
            d = (+1/6)*v1+(+4/6)*v2+(+1/6)*v3+(+0/6)*v4
            return a, b, c, d

    def get_delta(self):
        _d = 1/self.steps
        _d2, _d3 = _d**2, _d**3
        return _d, _d2, _d3
