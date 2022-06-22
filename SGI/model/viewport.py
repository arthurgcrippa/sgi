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
            pen.setWidthF(3)
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
            (x,y) = self.vp_trans(object.normalized[0], (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            visible = self.clipper.clip(object)
            if visible == 1:
                painter.drawPoint(x,y)
        elif (object.len() > 1):
            possible_lines = self.clipper.clip(object)
            if object.fill and object.len() > 2:
                points = self.clipper.get_points(possible_lines)
                points_vp = []
                first_point = self.vp_trans(points[0], (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
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
            else:
                for possible_line in possible_lines:
                    (p1, p2), visible = possible_line
                    (p1_x, p1_y) = self.vp_trans(p1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                    (p2_x, p2_y) = self.vp_trans(p2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                    if visible:
                        painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        self.update()
        painter.end()

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
            print("x: "+str(self.window.theta_x))
            print("y: "+str(self.window.theta_y))
            print("z: "+str(self.window.theta_z))
            matrix = Transformation3D(2, self.window.theta_x, (0,0,0), (0,0,0), 1, 1, object, None).normalize(object.matrix)
            matrix = Transformation3D(2, self.window.theta_y, (0,0,0), (0,0,0), 1, 2, object, None).normalize(matrix)
            matrix = Transformation3D(2, self.window.theta_z, (0,0,0), (0,0,0), 1, 3, object, None).normalize(matrix)
        else:
            Transformation2D(2, -self.window.theta_z, (0,0), object, None).normalize()

    def draw_axises(self):
        painter = self.get_painter(None)
        xMin, yMin, xMax, yMax = self.get_wc()
        vp_x, vp_y, vp_z = self.vpCoord[0]/2, self.vpCoord[1]/2, self.vpCoord[2]/2

        (x1, x2) = (0, vp_y, 0), (0, -vp_y, 0)
        (y1, y2) = (vp_x, 0, 0), (-vp_x, 0, 0)
        (z1, z2) = (0, 0, vp_z), (0, 0, -vp_z)

        theta_x, theta_y, theta_z = self.window.theta_x, self.window.theta_y, self.window.theta_z
        if theta_x != 0:
            matrix_y = matrices.rotation_x(theta_x, [[y1[0],y1[1], y1[2], 1], [y2[0],y2[1], y2[2], 1]])
            matrix_z = matrices.rotation_x(theta_x, [[z1[0],z1[1], z1[2], 1], [z2[0],z2[1], z2[2], 1]])
            y1 = (matrix_y[0][0], matrix_y[0][1], matrix_y[0][2])
            y2 = (matrix_y[1][0], matrix_y[1][1], matrix_y[1][2])
            z1 = (matrix_z[0][0], matrix_z[0][1], matrix_z[0][2])
            z2 = (matrix_z[1][0], matrix_z[1][1], matrix_z[1][2])
        if theta_y != 0:
            matrix_x = matrices.rotation_y(theta_y, [[x1[0],x1[1], x1[2], 1], [x2[0],x2[1], x2[2], 1]])
            matrix_z = matrices.rotation_y(theta_y, [[z1[0],z1[1], z1[2], 1], [z2[0],z2[1], z2[2], 1]])
            x1 = (matrix_x[0][0], matrix_x[0][1], matrix_x[0][2])
            x2 = (matrix_x[1][0], matrix_x[1][1], matrix_x[1][2])
            z1 = (matrix_z[0][0], matrix_z[0][1], matrix_z[0][2])
            z2 = (matrix_z[1][0], matrix_z[1][1], matrix_z[1][2])
        if theta_z != 0:
            matrix_x = matrices.rotation_z(theta_z, [[x1[0],x1[1], x1[2], 1], [x2[0],x2[1], x2[2], 1]])
            matrix_y = matrices.rotation_z(theta_z, [[y1[0],y1[1], y1[2], 1], [y2[0],y2[1], y2[2], 1]])
            x1 = (matrix_x[0][0], matrix_x[0][1], matrix_x[0][2])
            x2 = (matrix_x[1][0], matrix_x[1][1], matrix_x[1][2])
            y1 = (matrix_y[0][0], matrix_y[0][1], matrix_y[0][2])
            y2 = (matrix_y[1][0], matrix_y[1][1], matrix_y[1][2])



        (x1, x2), visible_x = self.clipper.line_clip(x1, x2)
        (y1, y2), visible_y = self.clipper.line_clip(y1, y2)
        (z1, z2), visible_z = self.clipper.line_clip(z1, z2)


        (p1_x, p1_y) = self.vp_trans(x1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = self.vp_trans(x2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        if visible_x:
            painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        (p1_x, p1_y) = self.vp_trans(y1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = self.vp_trans(y2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        if visible_y:
            painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        (p1_x, p1_y) = self.vp_trans(z1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = self.vp_trans(z2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        if visible_z:
            print("entrou aqui")
            coord = [p1_x, p1_y, p2_x, p2_y]
            print(coord)
            painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        self.update()
        painter.end()

    def move(self, index: int):
        self.window.move(index)
        self.redraw()

    def zoom_in(self):
        self.window.zoom(-1)
        self.redraw()

    def zoom_out(self):
        self.window.zoom(1)
        self.redraw()
