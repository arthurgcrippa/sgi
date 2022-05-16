from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import List
from model.form import Form

class Window():
    def __init__(self, viewPortHeight:int, viewPortWidth:int) -> None:
        super().__init__()
        self.xMin = - float(viewPortWidth/2)
        self.yMin = - float(viewPortHeight/2)
        self.xMax = float(viewPortWidth/2)
        self.yMax = float(viewPortHeight/2)
        self.theta = 0
        self.last_degree = 0

    def normalized(self) -> bool:
        return theta != 0

#   def pan(self, direction: str) -> None:
#         dist = 20
#         rad = -math.radians(self.theta)

#         if direction == 'up':
#             self.x_min -= math.sin(rad)*dist
#             self.x_max -= math.sin(rad)*dist
#             self.y_min += math.cos(rad)*dist
#             self.y_max += math.cos(rad)*dist

#         elif direction == 'down':
#             self.x_min += math.sin(rad)*dist
#             self.x_max += math.sin(rad)*dist
#             self.y_min -= math.cos(rad)*dist
#             self.y_max -= math.cos(rad)*dist

#         elif direction == 'right':
#             self.x_min += math.cos(rad)*dist
#             self.x_max += math.cos(rad)*dist
#             self.y_min += math.sin(rad)*dist
#             self.y_max += math.sin(rad)*dist

#         elif direction == 'left':
#             self.x_min -= math.cos(rad)*dist
#             self.x_max -= math.cos(rad)*dist
#             self.y_min -= math.sin(rad)*dist
#             self.y_max -= math.sin(rad)*dist

#         self.__update_center()

#     def __update_center(self):
#         center = ((self.x_max + self.x_min) / 2, (self.y_max + self.y_min) / 2)
#         self.center = center
