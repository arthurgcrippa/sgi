from form import Form
from viewport import Viewport

class Transformation():
    def __init__(self, type: int, axis: int, degree: float, object: Form, id: int) -> None:
        self.type = type
        self.axis = axis
        self.degree = degree
        self.object = object
        self.id = id

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

