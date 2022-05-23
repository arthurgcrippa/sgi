from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import Tuple, List
from model.form import Form
from model.window import Window
from model.transformation import Transformation
from model.coher_sutherland import CS_Clipper
from model.liang_barsky import LB_Clipper

import math
import numpy as np

t_coordinate = Tuple[float, float]

class Clipper():
    def __init__(self, window: Window, algorythm: int) -> None:
        self.window = window
        if algorythm == 0:
            self.clipper = CS_Clipper(self.window)
        elif algorythm == 1:
            self.clipper = LB_Clipper(self.window)

    def clip(self, object: Form):
        print("START CLIP")
        points = object.normalized
        print("Length: "+str(len(points)))
        if object.len() == 1:
            return self.point_clip(points[0])
        elif object.len() > 1:
            possible_lines = []
            object_lines = object.get_lines()
            for line in object_lines:
                possible_line = self.clipper.line_clip(line[0], line[1])
                possible_lines.append(possible_line)
            return possible_lines
        else:
            print("Object is Empty")
        return None

    def point_clip(self, point: t_coordinate):
        return self.point_visible(point)

    def point_visible(self, point: t_coordinate):
        left, bottom, right, top = self.get_wc()
        if point[0] < left or point[0] > right or point[1] < bottom or point[1] > top:
            return False #not visble
        return True #visible

    def line_clip(self, p1: t_coordinate, p2: t_coordinate):
        return self.clipper.line_clip(p1,p2)

    def get_wc(self):
        left = self.window.xMin
        bottom = self.window.yMin
        right = self.window.xMax
        top = self.window.yMax
        return left, bottom, right, top
