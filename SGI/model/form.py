from typing import List, Tuple
#from functools import cmp_to_key
#from PyQt5.QtGui import QPainter

t_coordinate = Tuple[float, float]

class Form():
    def __init__(self, name: str, coordinates: List[t_coordinate], id: int) -> None:
        self.name = name
        self.coordinates = coordinates
        self.id = id
        self.matrix = self.getMatrix(False)
        self.normalized = self.coordinates.copy()
        self.norm_matrix = self.getMatrix(False)
        # self.getMatrix()

    def add_cord(self, coordinate: t_coordinate):
        self.coordinates.append(coordinate)
        self.matrix = self.getMatrix()

    def len(self)->int:
        return len(self.coordinates)

    def get_center(self, norm: bool) -> t_coordinate:
        coordinates = self.coordinates
        if norm:
            coordinates = self.normalized
        x, y = (0,0)
        for coordinate in coordinates:
            x = x + coordinate[0]
            y = y + coordinate[1]
        x = x/self.len()
        y = y/self.len()
        return (x,y)

    # transformada de viewport
    def vp_trans(self, wCoord: t_coordinate, wMin: t_coordinate, wMax: t_coordinate, vpCoordinate: t_coordinate) -> t_coordinate:
        vp_x = ((wCoord[0] - wMin[0])/(wMax[0]-wMin[0]))*vpCoordinate[0]
        vp_y = (1-((wCoord[1]-wMin[1])/(wMax[1]-wMin[1])))*vpCoordinate[1]
        return (int(vp_x), int(vp_y))

    def setCoordinates(self, coordinates: List[t_coordinate], norm: bool):
        if norm:
            self.normalized = coordinates
        else:
            self.coordinates = coordinates

    def getMatrix(self, norm: bool) -> []:
        coordinates = self.coordinates
        if (norm):
            coordinates = self.normalized
        matrix = []
        for coordinate in coordinates:
            x, y = coordinate[0], coordinate[1]
            matrix.append([x,y,1])
        return matrix

    def setMatrix(self, matrix: [], norm: bool):
        if norm:
            self.norm_matrix = matrix
        else:
            self.matrix = matrix

    def reform(self, norm: bool):
        matrix = self.matrix
        coordinates = list()
        if norm:
            self.normalized.clear()
            matrix = self.norm_matrix
        else:
            self.coordinates.clear()
        for line in matrix:
            x, y = line[0], line[1]
            coordinates.append([x,y])
        if norm:
            self.setCoordinates(coordinates, True)
        else:
            self.setCoordinates(coordinates, False)
