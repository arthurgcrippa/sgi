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
        region_code = "0000"
        x, y = point[0], point[1]
        left, bottom, right, top = self.get_wc()

        if (x < left):
            region_code = "0001"
        elif (x > right):
            region_code = "0010"
        if (y < bottom):
            region_code = "0100"
        elif (y > top):
            region_code = "1000"

        return region_code

    def clip(self, object: Form):
        points = object.coordinates

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
                self.line_clip(p1,p2, object)
                stack.append(p2)
            p1 = points[0]
            p2 = points[len(points)-1]
            self.line_clip(p1,p2, object)
        else:
            print("Object is Empty")

    def point_clip(self, point: t_coordinate, object: Form):
        object.set_visible(self.point_visible(point))

    def line_clip(self, p1: t_coordinate, p2: t_coordinate, object: Form):
        scope = self.line_visible(p1, p2)
        if scope != 0:
            if scope == 1:
                object.set_visible(0)
            else:
                self.intersection(p1,p2,scope)
        else:
            object.set_visible(1)


    def point_visible(self, point: t_coordinate):
        rc = self.region_code(point)
        if self.bin_to_int(rc) != 0:
            return 1 #not visble
        return 0 #visible

    def line_visible(self, p1: t_coordinate, p2: t_coordinate):
        rc1 = self.bin_to_int(self.region_code(p1))
        rc2 = self.bin_to_int(self.region_code(p2))
        rc = self.bin_to_int(self.and_logico(rc1, rc2))
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
        regiao = []
        if scope == 2:
            regiao[0] = self.region_code(p2)
            
        if scope == 3:
            regiao[0] = self.region_code(p1)

        if scope == 4:
            regiao[0] = self.region_code(p1)
            regiao[1] = self.region_code(p2)

        return 0    
        
    def left_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = m*(left - p[0])+p[1]
        if new_point >= left & new_point <= right:
            new_coord = (left, new_point)
            return True
        else:
            return False 

    def bottom_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = (p[0] + 1/m) * (bottom - p[1])
        if new_point >= top & new_point <= bottom:
            new_coord = (new_point, bottom)
            return True
        else:
            return False 

    def right_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = m*(right - p[0])+p[1]
        if new_point >= left & new_point <= right:
            new_coord = (right, new_point)
            return True
        else:
            return False

    def top_inter(self, p: t_coordinate, m:int):
        left, bottom, right, top = self.get_wc()
        new_point = (p[0] + 1/m) * (top - p[1])
        if new_point >= top & new_point <= bottom:
            new_coord = (new_point, top)
            return True
        else:
            return False

    def int_to_bin(code: int):
        return '{0:04b}'.format(code)

    def bin_to_int(code: str):
        return int(code, 2)

    def and_logico(self, a: str, b: str):
        a_code = self.bin_to_int(a)
        b_code = self.bin_to_int(b)
        return self.int_to_bin((a_code & b_code))

    def ang_coef(self, p1: t_coordinate, p2:t_coordinate):
        return abs(p2[1] - p1[1])/(p2[0] - p1[0])
