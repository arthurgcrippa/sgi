from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import Tuple, List
from model.form import Form
from model.window import Window
from model.transformation import Transformation

import math
import numpy as np

t_coordinate = Tuple[float, float]

class CS_Clipper():
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

    def line_clip(self, p1: t_coordinate, p2: t_coordinate):
        scope = self.line_visible(p1, p2)
        if scope != 0:
            if scope == 1:
                return ((p1,p2), False)
            else:
                return self.intersection(p1,p2,scope)
        return ((p1,p2), True)

    def line_visible(self, p1: t_coordinate, p2: t_coordinate):
        rc1 = self.bin_to_int(self.region_code(p1))
        rc2 = self.bin_to_int(self.region_code(p2))
        rc = self.and_logico(rc1, rc2)
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
            possible_intersections = self.inter_shed(p2, m)
            for inter_point in possible_intersections:
                if inter_point != p1 and inter_point != p2:
                    p2 = inter_point
                    return ((p1,p2),True)
        if scope == 3:
            possible_intersections = self.inter_shed(p1, m)
            for inter_point in possible_intersections:
                if inter_point != p2 and inter_point != p1:
                    p1 = inter_point
                    return ((p1,p2),True)
        if scope == 4:
            possible_intersections_p1 = self.inter_shed(p1, m)
            for inter_point_p1 in possible_intersections_p1:
                if inter_point_p1 != p2 and inter_point_p1 != p1:
                    p1_new = inter_point_p1
                    possible_intersections_p2 = self.inter_shed(p2, m)
                    for inter_point_p2 in possible_intersections_p2:
                        if inter_point_p2 != p1 and inter_point_p2 != p2:
                            p2_new = inter_point_p2
                            return ((p1_new, p2_new), True)
        return ((p1,p2), False)

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
        return intersections

    def left_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = m*(left - p[0])+p[1]
        new_coord = (left, new_point)
        if new_point >= bottom and new_point <= top:
            return new_coord
        else:
            return p

    def bottom_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        if(m != float("inf")):
            new_point = p[0] + 1/m * (bottom - p[1])
        else:
            new_point = p[0]
        new_coord = (new_point, bottom)
        if new_point >= left and new_point <= right:
            return new_coord
        else:
            return p

    def right_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = m*(right - p[0])+p[1]
        new_coord = (right, new_point)
        if new_point >= bottom and new_point <= top:
            return new_coord
        else:
            return p

    def top_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        if(m != float("inf")):
            new_point = p[0] + 1/m * (top - p[1])
        else:
            new_point = p[0]
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
        if (p1[0] == p2[0]):
            return float('inf')
        return (p2[1] - p1[1])/(p2[0] - p1[0])
