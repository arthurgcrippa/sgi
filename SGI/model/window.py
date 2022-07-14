from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import List
from model.form import Form
from utils import matrices

ZOOM = 0.05

class Window():
    def __init__(self, width:int, height:int, depth:int) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.depth = depth
        self.xMin = - float(width/2)
        self.yMin = - float(height/2)
        self.zMin = - float(depth/2)
        self.xMax = float(width/2)
        self.yMax = float(height/2)
        self.zMax = float(depth/2)
        self.theta_x = 0
        self.theta_y = 0
        self.theta_z = 0
        self.projection_diff = 0

    def get_cop(self):
        cop = (0,0,-1000)
        diff = self.projection_diff
        cop_mat = [cop[0], cop[1], cop[2], 1]
        rotx_mat = matrices.rotation_x(self.theta_x, cop_mat)
        roty_mat = matrices.rotation_y(self.theta_y, rotx_mat)
        rotz_mat = matrices.rotation_z(self.theta_z, roty_mat)
        cop = (rotz_mat[0], rotz_mat[1], rotz_mat[2]+diff)
        return cop

    def update_window(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.xMin = - float(width/2)
        self.yMin = - float(height/2)
        self.zMin = - float(depth/2)
        self.xMax = float(width/2)
        self.yMax = float(height/2)
        self.zMax = float(depth/2)
        self.theta_x = 0
        self.theta_y = 0
        self.theta_z = 0
        self.projection_diff = 0

    def move(self, direction: int):
        diff_x, diff_y, diff_z = self.width/20, self.height/20, self.depth/20
        if direction == 1:
            self.yMin += diff_y
            self.yMax += diff_y
        elif direction == 2:
            self.yMin -= diff_y
            self.yMax -= diff_y
        elif direction == 3:
            self.xMin -= diff_x
            self.xMax -= diff_x
        elif direction == 4:
            self.xMin += diff_x
            self.xMax += diff_x
        elif direction == 5:
            self.zMin += diff_z
            self.zMax += diff_z
            self.projection_diff += diff_z
        elif direction == 6:
            self.zMin -= diff
            self.zMax -= diff
            self.projection_diff -= diff_z

    def zoom(self, sign):
        zoomX = self.width  * sign*ZOOM
        zoomY = self.height * sign*ZOOM
        zoomZ = self.depth  * sign*ZOOM
        if self.xMax-zoomX != self.xMin+zoomX:
            self.xMin += zoomX
            self.xMax -= zoomX
            self.yMin += zoomY
            self.yMax -= zoomY
            self.zMin += zoomZ
            self.zMax -= zoomZ
