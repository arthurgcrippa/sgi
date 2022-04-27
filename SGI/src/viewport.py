from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor

from typing import List

class Viewport(QLabel):
    def __init__(self, viewPortHeight:int, viewPortWidth:int) -> None:
        super().__init__()
        # self.viewPortHeight = viewPortHeight
        # self.viewPortWidth = viewPortWidth
        self.viewPortCoord = (viewPortWidth, viewPortHeight)

    def tamWindow(self, viewPortHeight: int, viewPortWidth: int) -> List[int]:
        self.xMin = - (viewPortWidth/2)
        self.yMin = - (viewPortHeight/2)
        self.xMax = viewPortWidth/2
        self.yMax = viewPortHeight/2
        return (self.xMin, self.yMin, self.xMax, self.yMax)



