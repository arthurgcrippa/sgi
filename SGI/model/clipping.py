from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import Tuple, List
from model.form import Form
from model.window import Window
from model.transformation import Transformation

import math
import numpy as np

t_coordinate = Tuple[float, float]

class Clipper():
    def __init__(self, window: Window) -> None:
        self.window = window

    def get_wc(self):
        left = self.window.xMin
        bottom = self.window.yMin
        right = self.window.xMax
        top = self.window.yMax
        return left, bottom, right, top

    def region_code(self, point: t_coordinate):
        region_code = 0 #0000
        x, y = point[0], point[1]
        left, bottom, right, top = self.get_wc()

        if (x < left):
            region_code = 1 #0001
        elif (x > right):
            region_code = 2 #0010
        if (y < bottom):
            region_code = region_code | 4 #0100
        elif (y > top):
            region_code = region_code | 8 #1000

        return self.int_to_bin(region_code)

    def clip(self, object: Form):
        points = object.normalized
        new_coordinates = []
        if object.len() == 1:
            self.point_clip(points[0], object)
        elif object.len() > 1:
            stack = []
            for p in points:
                if len(stack) == 0:
                    stack.append(p)
                    continue
                p1 = stack.pop()
                p2 = p
                new_p1, new_p2 = self.line_clip(p1,p2, object)
                new_coordinates.append(new_p1)
                new_coordinates.append(new_p2)
                stack.append(p2)
            p1 = points[0]
            p2 = points[len(points)-1]
            new_p1, new_p2 = self.line_clip(p1,p2, object)
            new_coordinates.append(new_p1)
            new_coordinates.append(new_p2)
        else:
            print("Object is Empty")
        return new_coordinates

    def point_clip(self, point: t_coordinate, object: Form):
        object.set_visible(self.point_visible(point))

    def line_clip(self, p1: t_coordinate, p2: t_coordinate, object: Form):
        scope = self.line_visible(p1, p2)
        if scope != 0:
            if scope == 1:
                object.set_visible(0)
            else:
                (p1, p2) = self.intersection(p1,p2,scope)
        else:
            object.set_visible(1)
        return (p1, p2)

    def point_visible(self, point: t_coordinate):
        rc = self.region_code(point)
        if self.bin_to_int(rc) != 0:
            return 1 #not visble
        return 0 #visible

    def line_visible(self, p1: t_coordinate, p2: t_coordinate):
        rc1 = self.bin_to_int(self.region_code(p1))
        rc2 = self.bin_to_int(self.region_code(p2))
        rc = self.and_logico(rc1, rc2)
        print("Coordenada 1: "+str(p1))
        print("Coordenada 2: "+str(p2))
        print("Region Code 1: "+ self.int_to_bin(rc1))
        print("Region Code 2: "+ self.int_to_bin(rc2))
        print("Region Code &: "+ str(rc))
        if rc1 != 0 or rc2 != 0:
            if rc == 0:
                if rc1 == 0:
                    return 2 #p1 within p2 outside scope
                elif rc2 == 0:
                    return 3 #p1 outside p2 witin scope
                elif rc1 != 0 and rc2 != 0:
                    return 4 #p1 & p2 outside scope
            else:
                return 1 #invisible
        return 0 #visible

    def intersection(self, p1: t_coordinate, p2: t_coordinate, scope: int):

        m = self.ang_coef(p1,p2)
        if scope == 2:
            intersections = self.inter_shed(p2, m)
            for inter in intersections:
                if inter != p1:
                    p2 = inter
        if scope == 3:
            intersections = self.inter_shed(p1, m)
            for inter in intersections:
                if inter != p2:
                    p1 = inter
        if scope == 4:
            intersections = self.inter_shed(p1, m)
            for inter in intersections:
                if inter != p2:
                    p1 = inter
            intersections = self.inter_shed(p2, m)
            for inter in intersections:
                if inter != p1:
                    p2 = inter
        return (p1,p2)

    def inter_shed(self, point: t_coordinate, m) -> List[t_coordinate]:
        quarter = self.region_code(point)
        intersections = []
        if quarter[0] == '1':
            intersections.append(self.top_inter(point, m))
        if quarter[1] == '1':
            intersections.append(self.bottom_inter(point, m))
        if quarter[2] == '1':
            intersections.append(self.right_inter(point, m))
        if quarter[3] == '1':
            intersections.append(self.left_inter(point, m))

    def left_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = m*(left - p[0])+p[1]
        new_coord = (left, new_point)
        if new_point >= left and new_point <= right:
            return new_coord
        else:
            return p

    def bottom_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = (p[0] + 1/m) * (bottom - p[1])
        new_coord = (new_point, bottom)
        if new_point >= left and new_point <= right:
            return new_coord
        else:
            return p

    def right_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = m*(right - p[0])+p[1]
        new_coord = (right, new_point)
        if new_point >= left and new_point <= right:
            return new_coord
        else:
            return p

    def top_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = (p[0] + 1/m) * (top - p[1])
        new_coord = (new_point, top)
        if new_point >= left and new_point <= right:
            return new_coord
        else:
            return p

    def int_to_bin(self, code: int):
        return '{0:04b}'.format(code)

    def bin_to_int(self, code: str):
        return int(code, 2)

    def and_logico(self, a: int, b: int):
        return (a & b)

    def ang_coef(self, p1: t_coordinate, p2:t_coordinate) -> int:
        return abs(p2[1] - p1[1])/(p2[0] - p1[0])
