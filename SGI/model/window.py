from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import List
from model.form import Form

MOVE = 30
ZOOM = 0.05

class Window():
    def __init__(self, vp_width:int, vp_height:int, vp_depth:int) -> None:
        super().__init__()
        self.vp_width = vp_width
        self.vp_height = vp_height
        self.vp_depth = vp_depth
        self.xMin = - float(vp_width/2)
        self.yMin = - float(vp_height/2)
        self.zMin = - float(vp_depth/2)
        self.xMax = float(vp_width/2)
        self.yMax = float(vp_height/2)
        self.zMax = float(vp_depth/2)
        self.theta = 0
        self.last_degree = 0

    def normalized(self) -> bool:
        return theta != 0

    def move(self, direction: int):
        diff = MOVE
        if direction == 1:
            self.yMin += diff
            self.yMax += diff
        elif direction == 2:
            self.yMin -= diff
            self.yMax -= diff
        elif direction == 3:
            self.xMin -= diff
            self.xMax -= diff
        elif direction == 4:
            self.xMin += diff
            self.xMax += diff
        elif direction == 5:
            self.zMin += diff
            self.zMax += diff
        elif direction == 6:
            self.zMin -= diff
            self.zMax -= diff

    def zoom(self, sign):
        zoomX = self.vp_width  * sign*ZOOM
        zoomY = self.vp_height * sign*ZOOM
        zoomZ = self.vp_depth  * sign*ZOOM
        self.xMin += zoomX
        self.xMax -= zoomX
        self.yMin += zoomY
        self.yMax -= zoomY
        self.zMin += zoomZ
        self.zMax -= zoomZ
