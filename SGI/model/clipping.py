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

    def clip(self, object: Form)
        points = object.coordinates

        if object.len() == 1:
            point_clip(points[0], object)
        elif object.len() > 1:
            stack = []
            for p in points:
                if len(stack) == 0:
                    stack.append(p)
                    continue
                p1 = stack.pop()
                p2 = p
                line_clip(p1,p2)
                stack.append(p2)
            p1 = points[0]
            p2 = points[len(pontos)-1]
            line_clip(p1,p2)
        else:
            print("Object is Empty")

    def point_clip(self, point: t_coordinate, object: Form):
        object.set_visible(self.point_visible(point))

    def line_clip(self, p1: t_coordinate, p2: t_coordinate):
        scope = self.line_visible(p1, p2)
        if scope != 0:
            self.intersection(p1,p2,scope)

    def point_visible(self, point: t_coordinate):
        rc = region_code(point)
        if bin_to_int(rc) != 0:
            return 1 #not visble
        return 0 #visible

    def line_visible(self, p1: t_coordinate, p2: t_coordinate):
        rc1 = bin_to_int(region_code(p1))
        rc2 = bin_to_int(region_code(p2))
        rc = bin_to_int(and(rc1, rc2))
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

    def intersection(self, p1: t_coordinate, p2: t_coordinate, scope: Int):
        left, bottom, right, top = self.get_wc()
    def left_inter(self, p1: coordinate, p2: t_coordinate):
        left, bottom, right, top = self.get_wc()

    def bottom_inter(self, p1: coordinate, p2: t_coordinate):
        left, bottom, right, top = self.get_wc()

    def right_inter(self, p1: coordinate, p2: t_coordinate):
        left, bottom, right, top = self.get_wc()

    def top_inter(self, p1: coordinate, p2: t_coordinate):
        left, bottom, right, top = self.get_wc()

    def int_to_bin(code: int):
        return '{0:04b}'.format(code)

    def bin_to_int(code: str):
        return int(code, 2)

    def and(a: str, b: str):
        a_code = bin_to_int(a)
        b_code = bin_to_int(b)
        return int_to_bin((a_code & b_code))
