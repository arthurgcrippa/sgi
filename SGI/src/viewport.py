from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import List
from form import Form

class Viewport(QLabel):
    def __init__(self, viewPortHeight:int, viewPortWidth:int) -> None:
        super().__init__()
        #self.viewPortHeight = viewPortHeight
        #self.viewPortWidth = viewPortWidth
        self.vpCoord = (int(viewPortWidth), int(viewPortHeight))
        self.pen_width = 3
        self.vp_init()

    def tamWindow(self, viewPortHeight: int, viewPortWidth: int) -> List[float]:
        xMin = - float(viewPortWidth/2)
        yMin = - float(viewPortHeight/2)
        xMax = float(viewPortWidth/2)
        yMax = float(viewPortHeight/2)
        return (xMin, yMin, xMax, yMax)

    def vp_init(self):
        board = QPixmap(self.vpCoord[0], self.vpCoord[1])
        board.fill(QColor('white'))
        self.setPixmap(board)
        self.board = self.pixmap()
        self.board.fill(QColor('white'))

    def draw(self, form: Form):
    # def draw(self):
        painter = QPainter(self.board)
        pen = QPen()
        pen.setWidthF(2)
        pen.setColor(QColor('black'))
        painter.setPen(pen)
        # painter.drawLine(1,1, 100,100)
        print("cehgou aqui")

        xMin, yMin, xMax, yMax = self.tamWindow(self.vpCoord[0], self.vpCoord[1])

        print(form.coordinates[0])
        print(form.coordinates[0][0])

        if (form.len() == 1):
            (x,y) = form.vp_trans(form.coordinates[0], (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
            painter.drawPoint(x,y)
        elif (len(form.coordinates) > 1):
            pontos = form.coordinates
            for p1 in pontos:
                for p2 in pontos:
                    (p1_x, p1_y) = form.vp_trans(p1, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                    (p2_x, p2_y) = form.vp_trans(p2, (xMin,yMin), (xMax,yMax), (self.vpCoord[0], self.vpCoord[1]))
                    painter.drawLine(p1_x, p1_y, p2_x, p2_y)
        self.update()
        painter.end()
