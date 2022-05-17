from typing import List, Tuple
from model.form import Form
from model.viewport import Viewport

class Descriptor():
    def __init__(self, viewport: Viewport) -> None:
        super().__init__()
        self.viewport = viewport
        self.write_random()

    def write_random(self):
        f = open('teste.txt', 'a')
        for obj in self.viewport.objectList:
            f.write('v ' + str(obj.coordinates) + '\n')
            # fazer outro for
            # fazer replace dos parenteses de abertura e fechamento
            # dar split pela virgula
            print()
        
        f.close

    
