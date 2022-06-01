from typing import Dict, List

from model.form import Form
from model.viewport import Viewport


def write(file_name: str, objList: List[Form]):
    vertices = []
    objMap = {}

    mtllib = file_name.split('.')[0] + "_colors.mtl"
    create_mtl(mtllib, objList)

    i = 0
    for obj in objList:
        vertices.extend(obj.coordinates)
        objMap[obj] = (i, i + len(obj.coordinates) - 1)
        i += len(obj.coordinates)

    f = open(file_name, "w")

    for v in vertices:
        line = "v " + str(v[0]) + " " + str(v[1]) + " 0.0\n"
        f.write(line)

    f.write("mtllib " + mtllib + "\n")

    for obj in objList:
        f.write("o " + obj.name + "\n")
        f.write("usemtl " + obj.name + "_mtl\n")
        line = pointsToString(obj, objMap)
        f.write(line)

    f.close()


def pointsToString(obj, objMap):
    pointSet3D = objMap[obj]
    line = ""
    if obj.len() == 1:
        line += "p "
    elif obj.len() == 2:
        line += "l "
    elif obj.len() > 2:
        if obj.fill:
            line+= "f "
        else:
            line+= "l "
    else:
        print("Objeto Vazio")

    for i in range(pointSet3D[0], pointSet3D[1] + 1):
        line += str(i + 1) + " "

    line += "\n"

    return line


def create_mtl(path, objList: List[Form]) -> None:
    mtl = open(path, "w")

    for obj in objList:
        mtl.write(create_name(obj))
        mtl.write(create_color(obj))

    mtl.close()


def create_name(obj: Form) -> str:
    line = "newmtl " + obj.name + "_mtl\n"
    return line


def create_color(obj: Form) -> str:
    r = "{:.6f}".format(obj.color[0] / 255)
    g = "{:.6f}".format(obj.color[1] / 255)
    b = "{:.6f}".format(obj.color[2] / 255)

    line = "Kd " + r + " " + g + " " + b + "\n\n"
    return line


def read(path):
    vertices = []
    objList = []
    watercolour = {}

    f = open(path, "r")
    line = f.readline().rstrip()
    line = line.split()
    while line:
        if line[0] == 'v':
            vertex = parse_vertex(line)
            vertices.append(vertex)

        if len(line[0]) > 1:
            watercolour = create_watercolor(line[1])

        if line[0] == 'o':
            obj = parse_object(line, f, watercolour)
            objList.append(obj)

        line = f.readline().rstrip()
        line = line.split()

    ###
    return create_forms(vertices, objList)


def parse_vertex(line):
    z = float(line.pop())
    y = float(line.pop())
    x = float(line.pop())
    return x, y, z


def parse_object(line, f, watercolour):
    obj = dict()

    name = line[1]
    line = f.readline().rstrip().split()[1]
    color = watercolour[line]
    line = f.readline().rstrip()
    line = line.split()

    if line[0] == 'p':
        vertex = [int(line[1])]
        obj["name"] = name
        obj["type"] = "Ponto"
        obj["color"] = color
        obj["vertices"] = vertex
        obj["fill"] = False

    elif line[0] == 'l':
        line.pop(0)
        vertices = []
        while line:
            vertices.append(int(line.pop()))
        obj["name"] = name
        obj["type"] = "Linha" if len(vertices) == 2 else "Poligono"
        obj["color"] = color
        obj["vertices"] = vertices
        obj["fill"] = False

    elif line[0] == 'f':
        line.pop(0)
        vertices = []
        while line:
            vertices.append(int(line.pop()))
        obj["name"] = name
        obj["type"] = "Linha" if len(vertices) == 2 else "Poligono"
        obj["color"] = color
        obj["vertices"] = vertices
        obj["fill"] = True

    return obj


def create_forms(vertices, objMapList):
    objList = list()
    id = 0
    for objMap in objMapList:
        pointSet3D = list()
        for v in objMap["vertices"]:
            pointSet3D.append(vertices[v - 1])
        obj = Form(objMap["name"], parse_3Dto2D(pointSet3D), id)
        obj.set_color(objMap["color"], 1)
        obj.set_fill(objMap["fill"])
        id += 1
        objList.append(obj)

    return objList

def parse_3Dto2D(pointSet3D):
    coordinates = list()
    for point3D in pointSet3D:
        x, y = point3D[0], point3D[1]
        coordinates.append((x,y))
    return coordinates

def create_watercolor(mtl_path) -> Dict:
    f = open(mtl_path, "r")
    watercolour = {}

    line = f.readline().rstrip()
    while line:
        if line[0] == 'n':
            mtl = line.rstrip().split()[1]
            srgb = f.readline().rstrip().split()[1:]
            watercolour[mtl] = string_to_rgb(srgb)

        line = f.readline().rstrip()
        line = f.readline().rstrip()

    f.close()
    return watercolour

def string_to_rgb(srgb: List[str]):
    r = int(float(srgb[0]) * 255)
    g = int(float(srgb[1]) * 255)
    b = int(float(srgb[2]) * 255)
    return r, g, b
