from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor, QPolygonF, QBrush, QPainterPath
from PyQt5.QtCore import *

from typing import List
from model.form import Form
from model.object2D import Object2D
from model.object3D import Object3D
from model.window import Window
from model.transformation import Transformation
from model.transformation2D import Transformation2D
from model.transformation3D import Transformation3D
from model.clipping import Clipper
from utils import matrices

import math
import numpy as np
import sys
class Viewport(QLabel):
    def __init__(self, vp_width:int, vp_height:int, vp_depth: int) -> None:
        super().__init__()
        self.vpCoord = (vp_width, vp_height, vp_depth)
        self.objectList: List[Form] = list()
        self.window = Window(vp_width, vp_height, vp_depth)
        self.clipper = Clipper(self.window, 0)
        self.vp_init()
        self.draw_axises()

    def vp_init(self):
        board = QPixmap(self.vpCoord[0]+20, self.vpCoord[1]+20)
        board.fill(QColor('white'))
        self.setPixmap(board)
        self.board = self.pixmap()
        self.board.fill(QColor('white'))

    def vp_trans(self, wCoord, wMin, wMax, vpCoordinate):
        vp_x = ((wCoord[0] - wMin[0])/(wMax[0]-wMin[0]))*vpCoordinate[0]
        vp_y = (1-((wCoord[1]-wMin[1])/(wMax[1]-wMin[1])))*vpCoordinate[1]
        return (int(vp_x), int(vp_y))

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
            pen.setWidthF(2)
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
        if object.grouped():
            for (group_lines, polygon) in object.get_group_lines():
                possible_lines = self.clipper.clip_lines(group_lines)
                if polygon:
                    points = self.clipper.get_points(possible_lines) #REVER SE POSSIVEL
                    self.draw_polygon(painter, possible_lines)
                else:
                    self.draw_wireframe(painter, possible_lines)
        else:
            if (object.len() == 1):
                (x,y) = self.vp_trans(object.normalized[0], (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                visible = self.clipper.clip(object)
                if visible == 1:
                    painter.drawPoint(x,y)
            elif (object.len() > 1):
                possible_lines = self.clipper.clip(object)
                if object.IS_POLYGON and object.len() > 2:
                    points = self.clipper.get_points(possible_lines)
                    self.draw_polygon(painter, points)
                else:
                    self.draw_wireframe(painter, possible_lines)
        self.update()
        painter.end()

    def draw_wireframe(self, painter, possible_lines):
        xMin, yMin, xMax, yMax = self.get_wc()
        for possible_line in possible_lines:
            (p1, p2), visible = possible_line
            (p1_x, p1_y) = self.vp_trans(p1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            (p2_x, p2_y) = self.vp_trans(p2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            if visible:
                painter.drawLine(p1_x, p1_y, p2_x, p2_y)

    def draw_polygon(self, painter, points):
        xMin, yMin, xMax, yMax = self.get_wc()
        object_path = QPainterPath()
        FIRST = True
        for point in points:
            point = self.vp_trans(point, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            if FIRST:
                object_path.moveTo(point[0], point[1])
                FIRST = False
                continue
            object_path.lineTo(point[0], point[1])
        painter.fillPath(object_path, painter.brush())

    def redraw(self):
        self.vp_init()
        self.draw_axises()
        for obj in self.objectList:
            self.draw(obj)

    def rotate_window(self, degree: int, orientation: int, axis: int):
        if orientation:
            degree *= -1
        if axis == 1:
            self.window.theta_x += degree
        elif axis == 2:
            self.window.theta_y += degree
        elif axis == 3:
            self.window.theta_z += degree
        self.redraw()

    def normalize(self, object: Form) -> None:
        if object.tridimentional():
            matrix = [object.matrix]
            theta_x, theta_y, theta_z = self.window.theta_x, self.window.theta_y, self.window.theta_z
            Transformation3D(2, theta_x, (0,0,0), (0,0,0), 1, 1, object, None).normalize(matrix)
            Transformation3D(2, theta_y, (0,0,0), (0,0,0), 1, 2, object, None).normalize(matrix)
            Transformation3D(2, theta_z, (0,0,0), (0,0,0), 1, 3, object, None).normalize(matrix)
            Transformation3D(4, None, self.window.get_cop(), None, None, None, object, None).normalize(matrix)
        else:
            Transformation2D(2, -self.window.theta_z, (0,0), object, None).normalize()


    def draw_axises(self):
        vp_x, vp_y, vp_z = self.vpCoord[0]/2, self.vpCoord[1]/2, self.vpCoord[2]/2
        axis_x = Object3D("eixo-x", [(vp_x, 0, 0), (-vp_x, 0, 0)], -1)
        axis_y = Object3D("eixo-y", [(0, vp_y, 0), (0, -vp_y, 0)], -2)
        axis_z = Object3D("eixo-z", [(0, 0, vp_z), (0, 0, -vp_z)], -3)
        axis_x.set_edges([([1,2], False)])
        axis_y.set_edges([([1,2], False)])
        axis_z.set_edges([([1,2], False)])
        axis_x.set_color("#ff0000", 0)
        axis_y.set_color("#00ff00", 0)
        axis_z.set_color("#0000ff", 0)
        self.draw(axis_x)
        self.draw(axis_y)
        self.draw(axis_z)


    def move(self, index: int):
        self.window.move(index)
        self.redraw()

    def zoom_in(self):
        self.window.zoom(-1)
        self.redraw()

    def zoom_out(self):
        self.window.zoom(1)
        self.redraw()
