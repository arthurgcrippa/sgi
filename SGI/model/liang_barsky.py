from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import Tuple, List
from model.form import Form
from model.window import Window
from model.transformation import Transformation

import math
import numpy as np

t_coordinate = Tuple[float, float]

class LB_Clipper():
    def __init__(self, window: Window) -> None:
        self.window = window

    def line_clip(self, p1: t_coordinate, p2: t_coordinate):
        delta_x = p2[0] - p1[0]
        delta_y = p2[1] - p1[1]
        p, q, zeta = [], [], []
        left, bottom, right, top = self.get_wc()
        visible = False
        p.append(-delta_x)
        p.append(delta_x)
        p.append(-delta_y)
        p.append(delta_y)
        q.append(p1[0] - left)
        q.append(right - p1[0])
        q.append(p1[1] - bottom)
        q.append(top - p1[1])
        z1 = 0
        z2 = 1
        for i in range(0, 4):
            if p[i] > 0:
                zeta_i = q[i]/p[i]
                zeta.append(zeta_i)
                z2 = min(z2, zeta_i)
            elif p[i]<0:
                zeta_i = q[i]/p[i]
                zeta.append(zeta_i)
                z1 = max(z1, zeta_i)
            elif(q[i] < 0):
                visible = False

        if(z1 == 0 and z2 == 0):
            visible = True
        if (z1 < z2):
            new_p1 = (p1[0]+z1*p[1], p1[1]+z1*p[3])
            new_p2 = (p1[0]+z2*p[1], p1[1]+z2*p[3])
            visible = True
            return ((new_p1,new_p2), visible)
        else:
            visible = False
        return ((p1,p2), visible)


    def get_wc(self):
        left = self.window.xMin
        bottom = self.window.yMin
        right = self.window.xMax
        top = self.window.yMax
        return left, bottom, right, top
