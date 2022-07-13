from typing import Dict, List, Tuple

from model.form import Form
from model.object2D import Object2D
from model.object3D import Object3D
from model.viewport import Viewport


def write(file_path: str, objList: List[Form]):
    vertices = []
    objMap = {}
    watercolour = {}

    i = 0
    for obj in objList:
        vertices.extend(obj.coordinates)
        objMap[obj] = (i, i + len(obj.coordinates) - 1)
        i += len(obj.coordinates)

        mtl = 'r' + str(obj.color[0]) + '_g' + str(obj.color[1]) + '_b' + str(obj.color[2])
        watercolour[obj.cor] = mtl

    obj_name = file_path.split('/').pop()
    mtl_name = obj_name.split('.')[0] + ".mtl"
    mtl_path = file_path.rstrip(obj_name) + mtl_name

    create_mtl(mtl_path, watercolour)

    f = open(file_path, "w")

    for v in vertices:
        line = "v " + "{:.1f}".format(v[0]) + " {:.1f}".format(v[1]) + " {:.1f}".format(v[2]) + "\n"
        f.write(line)

    f.write("mtllib " + mtl_name + "\n")

    for obj in objList:
        header = "g " if obj.grouped() else "o "
        f.write(header + obj.name + "\n")
        f.write("usemtl " + watercolour[obj.color] + "\n")
        lines = pointsToString(obj, objMap)
        for line in lines:
            f.write(line)

    f.close()


def pointsToString(obj, objMap):
    first, last = objMap[obj][0], objMap[obj][1]
    if obj.grouped():
        lines = []
        for circuit, polygon in obj.edges:
            line = ""
            header = "f " if polygon else "f "
            line += header
            for value in circuit:
                line += str(first+value)
            lines.append(line)
        return lines

    line = ""
    if obj.len() == 1:
        line += "p "
    elif obj.len() == 2:
        line += "l "
    elif obj.len() > 2:
        if obj.IS_POLYGON:
            line+= "f "
        else:
            line+= "l "
    else:
        print("Objeto Vazio")

    for i in range(first, last + 1):
        line += str(i + 1) + " "
    line += "\n"
    return [line]


def create_mtl(file_path, watercolour) -> None:
    # mtl = open("savefiles/"+file_path, "w")
    mtl = open(file_path, "w")

    for name, color in watercolour.items():
        mtl.write(create_name(name))
        mtl.write(create_color(color))

    mtl.close()

def create_name(name: str) -> str:
    line = "newmtl " + name + "\n"
    return line

def create_color(color: Tuple[float, float, float]) -> str:
    r = "{:.6f}".format(color[0] / 255)
    g = "{:.6f}".format(color[1] / 255)
    b = "{:.6f}".format(color[2] / 255)

    line = "Kd " + r + " " + g + " " + b + "\n\n"
    return line

def readline(f):
    return f.readline().decode('utf-8')



def read(file):
    vertices = []
    objList = []
    watercolour = {}
    name = file.split('/')[-1]
    lines = rawcount(file) + 1
    # with open("savefiles/"+file, "rb") as f:
    with open(file, "rb") as f:
        while True:
            if lines == 0:
                break
            line = readline(f)
            lines -= 1
            if line.rstrip():
                line = line.split()
                if line[0] == 'v':
                    vertex = parse_vertex(line)
                    vertices.append(vertex)

                elif line[0] == 'mtllib':
                    mtl = file.rstrip(name) + line[1]
                    watercolour = create_watercolor(mtl)

                elif line[0] == 'o':
                    obj = parse_object(line, f, watercolour)
                    if obj:
                        objList.append(obj)

                elif line[0] == 'g':
                    obj = parse_group(line, f, watercolour, lines) #TODO
                    if obj:
                        objList.append(obj)

    return create_forms(vertices, objList)


def parse_vertex(line):
    z = float(line.pop())
    y = float(line.pop())
    x = float(line.pop())
    return x, y, z


def parse_object(line, f, watercolour):
    obj = dict()
    color = [0,0,0]
    name = line[1]
    line = readline(f).rstrip().split()

    if line[0] == 'usemtl':
        color = watercolour[line[1]]
        line = readline(f).rstrip().split()

    if line[0] == 'p':
        return case_point(name, color, line, obj)

    elif line[0] == 'l':
        return case_line(name, color, line, obj)

    elif line[0] == 'f':
        return case_face(name, color, line, obj)

    elif line[0] == 'w':
        return case_window(name, color, line, obj)

    elif line[0] == 'bspline':
        return case_bspline(name, color, line, obj)

def parse_group(line, f, watercolour, lines):
    obj = dict()
    name = line[1]
    vertices = []
    edges = []
    index = 0
    color = [0,0,0]
    GROUP_SEQUENCE = True
    while True:
        line_b = readline(f)
        line = line_b.rstrip().split()
        if GROUP_SEQUENCE:
            if line[0] == "g":
                line_b = readline(f)
                line = line_b.rstrip().split()
            GROUP_SEQUENCE = False
        if line[0] in ["o", "g", "v"] or lines == 0:
            print(line_b)
            f.seek(-len(line_b),1)
            # line_b = readline(f)
            # print(line_b)
            break

        if line[0] == 'usemtl':
            color = watercolour[line[1]]
            line_b = readline(f)
            line = line_b.rstrip().split()

        elif line[0] == 'l':
            polygon = False
            line.pop(0)
            index = 0
            circuit = []
            for vertex in line:
                index += 1
                vertices.append(vertex)
                circuit.append(index)
            edges.append((circuit, polygon))

        elif line[0] == 'f':
            polygon = True
            line.pop(0)
            circuit = []
            first = index+1
            for vertex in line:
                index += 1
                vertices.append(vertex)
                circuit.append(index)
            circuit.append(first)
            edges.append((circuit, polygon))

    obj["name"] = name
    obj["type"] = "Group"
    obj["color"] = color
    obj["vertices"] = vertices
    obj["edges"] = edges
    return obj


def case_point(name, color, line, obj):
    vertex = [int(line[1])]
    obj["name"] = name
    obj["type"] = "Point"
    obj["color"] = color
    obj["vertices"] = vertex
    return obj

def case_line(name, color, line, obj):
    line.pop(0)
    vertices = []
    edges = []
    while line:
        vertices.append(int(line.pop()))

    index = 0
    circuit = []
    for v in vertices:
        index += 1
        circuit.append(index)
    edges.append((circuit, False))

    if len(vertices) == 2:
        obj["type"] = "Line"

    elif len(vertices) > 2:
        obj["type"] = "Wireframe"


    obj["name"] = name
    obj["color"] = color
    obj["vertices"] = vertices
    obj["edges"] = edges
    return obj

def case_face(name, color, line, obj):
    line.pop(0)
    vertices = []
    edges = []
    while line:
        vertices.append(int(line.pop()))
    index = 0
    circuit = []
    for v in vertices:
        index += 1
        circuit.append(index)
    edges.append((circuit, False))
    obj["name"] = name
    obj["type"] = "Polygon"
    obj["color"] = color
    obj["vertices"] = vertices
    obj["edges"] = edges
    return obj

def case_curve(name, color, line, obj):
    line.pop(0)
    vertices = []
    while line:
        vertices.append(int(line.pop()))
    obj["name"] = name
    obj["type"] = "Curve"
    obj["color"] = color
    obj["vertices"] = vertices
    return obj

def case_window(name, color, line, obj):
    line.pop(0)
    vertices = []
    while line:
        vertices.append(int(line.pop()))
    obj["name"] = name
    obj["type"] = "Window"
    obj["color"] = color
    obj["vertices"] = vertices
    return obj

def create_forms(vertices, objList):
    built = list()
    id = -1
    for obj in objList:
        id+=1
        points = list()
        for v in obj["vertices"]:
            points.append(vertices[int(v) - 1])
        if obj["type"] == "Point":
            p = Object3D(obj["name"], points, id)
            p.set_color(obj["color"], 1)
            built.append(p)

        elif obj["type"] == "Line":
            l = Object3D(obj["name"], points, id)
            l.set_color(obj["color"], 1)
            l.set_edges(obj["edges"])
            built.append(l)

        elif obj["type"] == "Wireframe":
            wf = Object3D(obj["name"], points, id)
            wf.set_color(obj["color"], 1)
            wf.set_edges(obj["edges"])
            built.append(wf)

        elif obj["type"] == "Polygon":
            pl = Object3D(obj["name"], points, id)
            pl.set_color(obj["color"], 1)
            pl.set_as_polygon(True)
            pl.set_edges(obj["edges"])
            built.append(pl)

        elif obj["type"] == "Curve":
            c = Object3D(obj["name"], points, id)
            c.set_color(obj["color"], 1)
            c.set_curvy(True)
            built.append(c)

        elif obj["type"] == "Group":
            g = Object3D(obj["name"], points, id)
            g.set_color(obj["color"], 1)
            g.set_edges(obj["edges"])
            built.append(g)

        elif obj["type"] == "Window":
            g = Object3D(obj["name"], points, id)
            g.set_color(obj["color"], 1)
            g.set_as_window(True)
            built.append(g)

    return built

def create_watercolor(file) -> Dict:
    watercolour = {}
    lines = rawcount(file) + 1
    # with open("savefiles/"+file, "r") as f:
    with open(file, "r") as f:
        for line in f:
            lines -= 1
            line = line.rstrip().split()
            if len(line) > 1 and line[0] == "newmtl":
                mtl = line[1]
                while line[0] != "Kd":
                    line = f.readline().rstrip().split()
                srgb = line[1:]
                watercolour[mtl] = string_to_rgb(srgb)
    return watercolour

def string_to_rgb(srgb: List[str]):
    r = int(float(srgb[0]) * 255)
    g = int(float(srgb[1]) * 255)
    b = int(float(srgb[2]) * 255)
    return r, g, b

def rawcount(filename):
    # f = open("savefiles/"+filename, 'rb')
    f = open(filename, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    f.close()
    return lines
