from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import List
from model.form import Form
from model.window import Window
from model.transformation import Transformation

import math
import numpy as np

class Viewport(QLabel):
    def __init__(self, viewPortHeight:int, viewPortWidth:int) -> None:
        super().__init__()
        self.vpCoord = (int(viewPortWidth), int(viewPortHeight))
        self.objectList: List[Form] = list()
        self.window = Window(viewPortHeight, viewPortWidth)
        self.vp_init()
        self.draw_axises(Form)

    def vp_init(self):
        board = QPixmap(self.vpCoord[0]+20, self.vpCoord[1]+20)
        board.fill(QColor('white'))
        self.setPixmap(board)
        self.board = self.pixmap()
        self.resize(self.vpCoord[0]+10, self.vpCoord[1]+10)
        self.board.fill(QColor('white'))

    def draw(self, form: Form):
        self.normalize(form)
        painter = QPainter(self.board)
        pen = QPen()
        pen.setWidthF(4)
        r = form.color[0]
        g = form.color[1]
        b = form.color[2]
        pen.setColor(QColor(r,g,b))
        painter.setPen(pen)

        self.normalize(form)

        xMin = self.window.xMin
        yMin = self.window.yMin
        xMax = self.window.xMax
        yMax = self.window.yMax
        if (form.len() == 1):
            (x,y) = form.vp_trans(form.normalized[0], (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            painter.drawPoint(x,y)
        elif (len(form.coordinates) > 1):
            pontos = form.normalized
            stack = []
            for p in pontos:
                if len(stack) == 0:
                    stack.append(p)
                    continue
                p1 = stack.pop()
                p2 = p
                (p1_x, p1_y) = form.vp_trans(p1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                (p2_x, p2_y) = form.vp_trans(p2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                painter.drawLine(p1_x, p1_y, p2_x, p2_y)
                stack.append(p2)
            p1 = pontos[0]
            p2 = pontos[len(pontos)-1]
            (p1_x, p1_y) = form.vp_trans(p1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            (p2_x, p2_y) = form.vp_trans(p2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
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
        rotation_norm = Transformation(2, -degree, (0,0), form, None)
        rotation_norm.normalize()

    def draw_axises(self, form: Form):
        painter = QPainter(self.board)
        pen = QPen()
        pen.setWidthF(1)
        pen.setColor(QColor('black'))
        painter.setPen(pen)

        xMin = self.window.xMin
        yMin = self.window.yMin
        xMax = self.window.xMax
        yMax = self.window.yMax

        theta = -math.radians(self.window.theta)
        sin = np.sin(theta)
        cos = np.cos(theta)
        vp_x, vp_y = self.vpCoord[0]/2, self.vpCoord[1]/2
        x1 = (0, vp_y)
        x2 = (0, -vp_y)
        y1 = (vp_x, 0)
        y2 = (-vp_x, 0)

        if (self.window.theta != 0):
            x1 = (vp_x*sin, vp_y*cos)
            x2 = (-vp_x*sin, -vp_y*cos)
            y1 = (vp_x*cos, -vp_y*sin)
            y2 = (-vp_x*cos, vp_y*sin)


        (p1_x, p1_y) = form.vp_trans(self, x1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = form.vp_trans(self, x2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        (p1_x, p1_y) = form.vp_trans(self, y1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = form.vp_trans(self, y2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        painter.drawLine(p1_x, p1_y, p2_x, p2_y)

        self.update()
        painter.end()

    def move(self, index: int):
        diff = 50
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
