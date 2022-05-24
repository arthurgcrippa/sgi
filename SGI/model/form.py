from typing import List, Tuple

t_coordinate = Tuple[float, float]

class Form():
    def __init__(self, name: str, coordinates: List[t_coordinate], id: int) -> None:
        self.name = name
        self.coordinates = coordinates
        self.id = id
        self.matrix = self.getMatrix()
        self.normalized = self.coordinates.copy()
        self.color = [0,0,0]
        self.fill = 1

    def set_color(self, color):
        self.color = color

    def set_visible(self, visible):
        self.visible = visible

    def add_cord(self, coordinate: t_coordinate):
        self.coordinates.append(coordinate)
        self.matrix = self.getMatrix()

    def len(self)->int:
        return len(self.coordinates)

    def get_center(self) -> t_coordinate:
        coordinates = self.coordinates
        x, y = (0,0)
        for coordinate in coordinates:
            x = x + coordinate[0]
            y = y + coordinate[1]
        x = x/self.len()
        y = y/self.len()
        return (x,y)

    def get_lines(self):
        object_lines = []
        stack = []
        points = self.normalized
        for p in points:
            if len(stack) == 0:
                stack.append(p)
                continue
            p1 = stack.pop()
            p2 = p
            object_lines.append((p1,p2))
            stack.append(p2)
        p2 = points[0]
        p1 = points[len(points)-1]
        object_lines.append((p1,p2))
        return object_lines

    def get_points(self, possible_lines):
        points = []
        for line, visible in possible_lines:
            if visible:
                if line[0] not in points:
                    points.append(line[0])
                if line[1] not in points:
                    points.append(line[1])
        if len(points) > 0:
            points.append(points[0])
        return points

    # transformada de viewport
    def vp_trans(self, wCoord: t_coordinate, wMin: t_coordinate, wMax: t_coordinate, vpCoordinate: t_coordinate) -> t_coordinate:
        vp_x = ((wCoord[0] - wMin[0])/(wMax[0]-wMin[0]))*vpCoordinate[0]
        vp_y = (1-((wCoord[1]-wMin[1])/(wMax[1]-wMin[1])))*vpCoordinate[1]
        return (int(vp_x), int(vp_y))

    def setCoordinates(self, coordinates: List[t_coordinate]):
        self.coordinates = coordinates

    def getMatrix(self) -> []:
        coordinates = self.coordinates
        matrix = []
        for coordinate in coordinates:
            x, y = coordinate[0], coordinate[1]
            matrix.append([x,y,1])
        return matrix

    def setMatrix(self, matrix: []):
        self.matrix = matrix

    def reform(self):
        matrix = self.matrix
        self.coordinates.clear()
        for line in matrix:
            x, y = line[0], line[1]
            self.coordinates.append([x,y])
