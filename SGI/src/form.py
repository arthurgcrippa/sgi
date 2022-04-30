from typing import List, Tuple
from functools import cmp_to_key
from PyQt5.QtGui import QPainter

t_coordinate = Tuple[float, float]

class Form():
    def __init__(self, name: str, coordinates: List[t_coordinate]) -> None:
        self.name = name
        self.coordinates = coordinates
        print('TESTES SUPREMOS:')
        print(coordinates[0])
        print(self.coordinates[0])

    def add_cord(self, coordinate: t_coordinate):
        self.coordinates.append(coordinate)

    def len(self)->int:
        return len(self.coordinates)

    # transformada de viewport
    def vp_trans(self, wCoord: t_coordinate, wMin: t_coordinate, wMax: t_coordinate, vpCoordinate: t_coordinate) -> t_coordinate:
        print('TESTES:')
        print(wMin[0])
        print(wMin[1])
        print(wMax[0])
        print(wMax[1])
        print(wCoord[0])
        print(wCoord[1])
        print(vpCoordinate[0])
        print(vpCoordinate[1])
        vp_x = ((wCoord[0] - wMin[0])/(wMax[0]-wMin[0]))*vpCoordinate[0]
        vp_y = (1-((wCoord[1]-wMin[1])/(wMax[1]-wMin[1])))*vpCoordinate[1]
        return (vp_x, vp_y)
