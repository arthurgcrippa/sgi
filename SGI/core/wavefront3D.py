from typing import Dict, List

from model.form import Form
from model.object2D import Object2D
from model.viewport import Viewport


def write(file_path: str, objList: List[Form]):
    vertices = []
    objMap = {}
    watercolour = {}

    i = 0
    for obj in objList:
        vertices.extend(obj.coordinates)
        objMap[obj] = (i, i + len(obj.coordinates) - 1)
        i += len(obj.pontos)

        mtl = 'r' + str(obj.color[0]) + '_g' + str(obj.color[1]) + '_b' + str(obj.color[2])
        watercolour[obj.cor] = mtl

    obj_name = file_path.split('/').pop()
    mtl_name = obj_name.split('.')[0] + ".mtl"
    mtl_path = file_path.rstrip(obj_name) + mtl_name

    __create_mtl_file(mtl_path, watercolour)

    f = open(file_path, "w")

    for v in vertices:
        line = "v " + "{:.1f}".format(v[0]) + " {:.1f}".format(v[1]) + " {:.1f}".format(v[2]) + "\n"
        f.write(line)

    f.write("mtllib " + mtl_name + "\n")

    for obj in objList:
        f.write("o " + obj.name + "\n")
        f.write("usemtl " + watercolour[obj.color] + "\n")
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

    for i in range(points[0], points[1] + 1):
        line += str(i + 1) + " "

    if obj.wireframe: #TODO
        line += str(points[0] + 1)
    line += "\n"
    return line


def create_mtl(file_path, watercolour) -> None:
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


def read(file):
    vertices = []
    objList = []
    watercolour = {}
    name = file.split('/')[-1]
    lines = rawcount(file) + 1

    with open(file, "r") as f:
        for line in f:
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

                elif line[0] in {'f', 'l'}:
                    obj = __parse_unique(line, f, name.rstrip('.obj'), lines) #TODO
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

    name = line[1]
    line = f.readline().rstrip().split()

    if line[0] == 'usemtl':
        color = watercolour[line[1]]
        line = f.readline().rstrip().split()

    if line[0] == 'p':
        return case_point(name, color, line, obj)

    elif line[0] == 'l':
        return case_line(name, color, line, obj)

    elif line[0] == 'f':
        return case_face(name, color, line, obj, True)


def case_point(name, color, line, obj):
    vertex = [int(line[1])]
    obj["name"] = name
    obj["type"] = "Ponto"
    obj["color"] = color
    obj["vertices"] = vertex
    return obj

def case_line(name, color, line, obj):
    line.pop(0)
    vertices = []
    while line:
        vertices.append(int(line.pop()))

    if len(vertices) == 2:
        obj["type"] = "Linha"

    elif vertices[0] == vertices[len(vertices) - 1]:
        obj["type"] = "Wireframe" #TODO
        vertices.pop() # REMOVER OS VERTICES REPETIDOS OU NÃO

    else:
        obj["type"] = "Curva"

    obj["name"] = name
    obj["color"] = color
    obj["vertices"] = vertices
    return obj

def case_face(name, color, line, obj, fill):
    line.pop(0)
    vertices = []
    while line:
        vertices.append(int(line.pop()))
    obj["name"] = name
    obj["type"] = "Poligono" if fill else "Wireframe"
    obj["color"] = color
    obj["vertices"] = vertices
    return obj


# objeto composto por linhas e faces
def parse_compound(line, f, name, lines):
    father = dict()
    objects = list()
    id = 0

    # cria primeira f
    obj = dict()
    id += 1
    name += '_f_' + str(id)
    objects.append(__case_f(name, (0,0,0), line, obj, False))

    # cria demais f's até o fim do arquivo ou encontrar algo que nao seja 'f'
    while lines:
        lines -= 1
        line = f.readline().rstrip().split()
        if line[0] in {'f', 'l'}:
            obj = dict()
            id += 1
            name = obj_name + '_f_' + str(id)
            objects.append(__case_f(name, (0,0,0), line, obj, False))
        else:
            break

    father["name"] = name
    father["type"] = "Composto"
    father["objects"] = objects
    return father


def create_forms(vertices, objList):
    built = list()
    id = -1
    for obj in objList:
        id+=1
        if obj["type"] is "Composto":
            objects = create_forms(vertices, obj['objects']) # chamada recursiva....
            g = Grupo(obj['name'], objects, (0,0,0))
            built.append(g)
        else:
            points = list()
            for v in obj["vertices"]:
                points.append(vertices[v - 1])

            if obj["type"] is "Ponto":
                p = Object3D(obj["name"], points, id)
                p.set_color(obj["color"])
                built.append(p)

            elif obj["type"] is "Linha":
                l = Object3D(obj["name"], points, id)
                l.set_color(obj["color"])
                built.append(l)

            elif obj["type"] is "Wireframe":
                wf = Object3D(obj["name"], points, id)
                wf.set_color(obj["color"])
                built.append(wf)

            elif obj["type"] is "Poligono":
                pl = Object3D(obj["name"], points, id)
                pl.set_color(obj["color"])
                pl.set_fill(True)
                built.append(pl)

            elif obj["type"] is "Curva":
                c = Object2D(obj["name"], points, id)
                c.set_color(obj["color"])
                c.set_curvy(True)
                built.append(c)

    return built

def create_watercolor(file) -> Dict:
    f = open(file, "r")
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

def rawcount(filename):
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
