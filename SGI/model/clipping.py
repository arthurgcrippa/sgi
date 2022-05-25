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
float_error = 0.01

class Clipper():
    def __init__(self, window: Window, algorythm: int) -> None:
        self.window = window
        if algorythm == 0:
            self.clipper = CS_Clipper(self.window)
        elif algorythm == 1:
            self.clipper = LB_Clipper(self.window)

    def clip(self, object: Form):
        points = object.normalized
        if object.len() == 1:
            return self.point_clip(points[0])
        elif object.len() > 1:
            possible_lines = []
            object_lines = object.get_lines()
            for line in object_lines:
                possible_line = self.clipper.line_clip(line[0], line[1])
                possible_lines.append(possible_line)
            return possible_lines
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

    def get_points(self, possible_lines):
        points = []
        visible_segment = True
        segment_until_visible = []
        for line, visible in possible_lines:
            segment_until_visible.append((line, visible))
            if visible:
                break
        for possible_line in segment_until_visible:
            possible_lines.append(possible_line)
        first_visible_point = None
        last_visible_point = None
        for line, visible in possible_lines:
            if visible:
                if  not visible_segment:
                    first_visible_point = line[0]
                    if last_visible_point != None:
                        (p1, p2) = (last_visible_point, first_visible_point)
                        if (p1[0] != p2[0]) and (p1[1] != p2[1]):
                            for border_point in self.get_border():
                                if p1[0] == border_point[0] and p2[1] == border_point[1]:
                                    points.append(border_point)
                                if p1[1] == border_point[1] and p2[0] == border_point[0]:
                                    points.append(border_point)
                        first_visible_point = None
                        last_visible_point = None
                if line[0] not in points:
                    points.append(line[0])
                if line[1] not in points:
                    points.append(line[1])
                last_visible_point = line[1]
                visible_segment = visible
            else:
                visible_segment = False

        if len(points) > 0:
            points.append(points[0])
        return points

    def get_wc(self):
        left = self.window.xMin - float_error
        bottom = self.window.yMin - float_error
        right = self.window.xMax + float_error
        top = self.window.yMax + float_error
        return left, bottom, right, top

    def get_border(self):
        left, bottom, right, top = self.get_wc()
        p1, p2, p3, p4 = (left, top), (right, top), (right, bottom), (left, bottom)
        return [p1, p2, p3, p4]
