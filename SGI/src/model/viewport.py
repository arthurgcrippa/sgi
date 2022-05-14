from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import List
from model.form import Form

class Viewport(QLabel):
    def __init__(self, viewPortHeight:int, viewPortWidth:int) -> None:
        super().__init__()
        self.vpCoord = (int(viewPortWidth), int(viewPortHeight))
        self.objectList: List[Form] = list()
        self.pen_width = 3
        self.tamWindow(viewPortHeight, viewPortWidth)
        self.vp_init()
        self.draw_axes(Form)

    def tamWindow(self, viewPortHeight: int, viewPortWidth: int):
        self.xMin = - float(viewPortWidth/2)
        self.yMin = - float(viewPortHeight/2)
        self.xMax = float(viewPortWidth/2)
        self.yMax = float(viewPortHeight/2)

    def vp_init(self):
        board = QPixmap(self.vpCoord[0], self.vpCoord[1])
        board.fill(QColor('white'))
        self.setPixmap(board)
        self.board = self.pixmap()
        self.board.fill(QColor('white'))

    def draw(self, form: Form):
        painter = QPainter(self.board)
        pen = QPen()
        pen.setWidthF(2)
        pen.setColor(QColor('black'))
        painter.setPen(pen)

        xMin = self.xMin
        yMin = self.yMin
        xMax = self.xMax
        yMax = self.yMax

        if (form.len() == 1):
            (x,y) = form.vp_trans(form.coordinates[0], (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            painter.drawPoint(x,y)
        elif (len(form.coordinates) > 1):
            pontos = form.coordinates
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
        self.draw_axes(Form)
        for obj in self.objectList:
            self.draw(obj)

    def draw_axes(self, form: Form):
        painter = QPainter(self.board)
        pen = QPen()
        pen.setWidthF(1)
        pen.setColor(QColor('black'))
        painter.setPen(pen)

        xMin = self.xMin
        yMin = self.yMin
        xMax = self.xMax
        yMax = self.yMax

        (p1_x, p1_y) = form.vp_trans(self, (0, 10000), (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = form.vp_trans(self, (0, -10000), (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        painter.drawLine(p1_x, p1_y, p2_x, p2_y)

        (p1_x, p1_y) = form.vp_trans(self, (10000, 0), (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        (p2_x, p2_y) = form.vp_trans(self, (-10000, 0), (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
        painter.drawLine(p1_x, p1_y, p2_x, p2_y)

        self.update()
        painter.end()

    def move(self, index: int):
        diff = 50
        if index == 1:
            self.yMin = self.yMin + diff
            self.yMax = self.yMax + diff
        elif index == 2:
            self.yMin = self.yMin - diff
            self.yMax = self.yMax - diff
        elif index == 3:
            self.xMin = self.xMin - diff
            self.xMax = self.xMax - diff
        elif index == 4:
            self.xMin = self.xMin + diff
            self.xMax = self.xMax + diff
        self.redraw()

    def zoom_out(self):
        zoomVar = 0.05

        zoomX = self.vpCoord[0] * zoomVar
        zoomY = self.vpCoord[1] * zoomVar

        self.xMax = self.xMax - zoomX  
        self.xMin = self.xMin + zoomX
        self.yMax = self.yMax - zoomY
        self.yMin = self.yMin + zoomY

        self.redraw()

    def zoom_in(self):
        zoomVar = -0.05

        zoomX = self.vpCoord[0] * zoomVar
        zoomY = self.vpCoord[1] * zoomVar

        self.xMax = self.xMax - zoomX  
        self.xMin = self.xMin + zoomX
        self.yMax = self.yMax - zoomY
        self.yMin = self.yMin + zoomY

        self.redraw()