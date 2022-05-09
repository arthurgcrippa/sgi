from form import Form
from viewport import Viewport
from typing import Tuple

t_coordinate = Tuple[float, float]

class Transformation():
    # ROTAÇÃO
    def __init__(self, type: int, axis: int, degree: float, object: Form, id: int, point: t_coordinate) -> None:
        self.type = type
        self.axis = axis
        self.degree = degree
        self.object = object
        self.id = id
        self.point = point

    # TRANSLAÇÃO
    def __init__(self, type: int, point_diff: t_coordinate, object: Form, id: int) -> None:
        self.type = type
        self.point_diff = point_diff
        self.object = object
        self.id = id

    # ESCALONAMENTO
    def __init__(self, type: int, escale: int, object: Form, id: int) -> None:
        self.type = type
        self.object = object
        self.id = id
        self.escale = escale

    def transform(self):
        if self.type == 1:
            self.translation()
        elif self.type == 2:
            self.rotation()
        elif self.type == 3:
            self.escalonamento()
        

    def translation(self):
        return 0

    def rotation(self):
        return 0

    def escalonamento(self):
        return 0

