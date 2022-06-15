from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor, QPolygonF, QBrush, QPainterPath
from PyQt5.QtCore import *

from typing import List
from model.form import Form
from model.window import Window
from model.transformation import Transformation
from model.clipping import Clipper

import math
import numpy as np

class Viewport(QLabel):
    def __init__(self, viewPortHeight:int, viewPortWidth:int) -> None:
        super().__init__()
        self.vpCoord = (int(viewPortWidth), int(viewPortHeight))
        self.objectList: List[Form] = list()
        self.window = Window(viewPortHeight, viewPortWidth)
        self.clipper = Clipper(self.window, 0)
        self.vp_init()
        self.draw_axises(Form)

    def vp_init(self):
        board = QPixmap(self.vpCoord[0]+20, self.vpCoord[1]+20)
        board.fill(QColor('white'))
        self.setPixmap(board)
        self.board = self.pixmap()
        self.board.fill(QColor('white'))

    def get_wc(self):
        xMin = self.window.xMin
        yMin = self.window.yMin
        xMax = self.window.xMax
        yMax = self.window.yMax
        return xMin, yMin, xMax, yMax

    def get_painter(self, object: Form):
        painter = QPainter(self.board)
        pen = QPen()
        brush = QBrush()
        if object == None:
            pen.setWidthF(1)
            pen.setColor(QColor('black'))
        else:
            r = object.color[0]
            g = object.color[1]
            b = object.color[2]
            pen.setWidthF(1)
            pen.setColor(QColor(r,g,b))
            brush.setColor(QColor(r,g,b))
            brush.setStyle(Qt.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(brush)
        return painter

    def draw(self, object: Form):

        self.normalize(object)
        painter = self.get_painter(object)
        xMin, yMin, xMax, yMax = self.get_wc()
        if (object.len() == 1):
            (x,y) = object.vp_trans(object.normalized[0], (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            visible = self.clipper.clip(object)
            if visible == 1:
                print("Point: x = "+str(x)+" y = "+str(y))
                painter.drawPoint(x,y)
        elif (object.len() > 1):
            possible_lines = self.clipper.clip(object)
            if object.fill and object.len() > 2:
                points = self.clipper.get_points(possible_lines)
                points_vp = []
                first_point = object.vp_trans(points[0], (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                object_path = QPainterPath()
                FIRST = True
                for point in points:
                    point = object.vp_trans(point, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                    if FIRST:
                        object_path.moveTo(point[0], point[1])
                        FIRST = False
                        continue
                    object_path.lineTo(point[0], point[1])
                painter.fillPath(object_path, painter.brush())
            else:
                for possible_line in possible_lines:
                    (p1, p2), visible = possible_line
                    (p1_x, p1_y) = object.vp_trans(p1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                    (p2_x, p2_y) = object.vp_trans(p2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                    if visible:
                        painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        self.update()
        painter.end()

    def redraw(self):
        self.vp_init()
        self.draw_axises(Form)
        for obj in self.objectList:
            self.draw(obj)

    def rotate_window(self, degree: int, orientation: int):
        if orientation:
            degree *= -1
        self.window.theta += degree
        self.redraw()

    def normalize(self, form: Form) -> None:
        degree = self.window.theta
        rotation_norm = Transformation(4, -degree, (0,0,0), form, None)
        rotation_norm.normalize()

    def draw_axises(self, form: Form):
        painter = self.get_painter(None)
        xMin, yMin, xMax, yMax = self.get_wc()

        theta = -math.radians(self.window.theta)
        sin = np.sin(theta)
        cos = np.cos(theta)
        vp_x, vp_y = self.vpCoord[0]/2, self.vpCoord[1]/2

        (x1, x2) = (0, vp_y), (0, -vp_y)
        (y1, y2) = (vp_x, 0), (-vp_x, 0)

        if (self.window.theta != 0):
            x1 = (vp_x*sin, vp_y*cos)
            x2 = (-vp_x*sin, -vp_y*cos)
            y1 = (vp_x*cos, -vp_y*sin)
            y2 = (-vp_x*cos, vp_y*sin)

        (x1, x2), visible_x = self.clipper.line_clip(x1, x2)
        (y1, y2), visible_y = self.clipper.line_clip(y1, y2)


        (p1_x, p1_y) = form.vp_trans(self, x1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = form.vp_trans(self, x2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        if visible_x:
            # print("x1: "+str(p1_x))
            # print("y1: "+str(p1_y))
            # print("x2: "+str(p2_x))
            # print("y2: "+str(p2_y))
            painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        (p1_x, p1_y) = form.vp_trans(self, y1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = form.vp_trans(self, y2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        if visible_y:
            # print("x1: "+str(p1_x))
            # print("y1: "+str(p1_y))
            # print("x2: "+str(p2_x))
            # print("y2: "+str(p2_y))
            painter.drawLine(p1_x, p1_y, p2_x, p2_y)

        self.update()
        painter.end()

    def move(self, index: int):
        diff = 30
        if index == 1:
            self.window.yMin = self.window.yMin + diff
            self.window.yMax = self.window.yMax + diff
        elif index == 2:
            self.window.yMin = self.window.yMin - diff
            self.window.yMax = self.window.yMax - diff
        elif index == 3:
            self.window.xMin = self.window.xMin - diff
            self.window.xMax = self.window.xMax - diff
        elif index == 4:
            self.window.xMin = self.window.xMin + diff
            self.window.xMax = self.window.xMax + diff
        self.redraw()

    def zoom_out(self):
        zoomVar = 0.05

        zoomX = self.vpCoord[0] * zoomVar
        zoomY = self.vpCoord[1] * zoomVar

        self.window.xMax = self.window.xMax - zoomX
        self.window.xMin = self.window.xMin + zoomX
        self.window.yMax = self.window.yMax - zoomY
        self.window.yMin = self.window.yMin + zoomY

        self.redraw()

    def zoom_in(self):
        zoomVar = -0.05

        zoomX = self.vpCoord[0] * zoomVar
        zoomY = self.vpCoord[1] * zoomVar

        self.window.xMax = self.window.xMax - zoomX
        self.window.xMin = self.window.xMin + zoomX
        self.window.yMax = self.window.yMax - zoomY
        self.window.yMin = self.window.yMin + zoomY

        self.redraw()
