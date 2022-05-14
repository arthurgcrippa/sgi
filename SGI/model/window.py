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

    def alguma_coisa():
        return 0
        