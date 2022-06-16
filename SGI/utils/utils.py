
def parse_input(plaintext: str, floating: bool):
    coordinates = []
    for co_str in plaintext.split(";"):
        co_str = co_str.replace("(", "").replace(")", "")
        co = co_str.split(",")
        if len(co) == 2:
            if floating:
                x,y = float(co[0]), float(co[1])
                coordinates.append((x,y))
            else:
                x,y = int(co[0]), int(co[1])
                coordinates.append((x,y))
        elif len(co) == 3:
            if floating:
                x,y,z = float(co[0]), float(co[1]), float(co[2])
                coordinates.append((x,y,z))
            else:
                x,y,z = int(co[0]), int(co[1]), int(co[2])
                coordinates.append((x,y,z))
    return coordinates

def parse_float(plaintext: str):
    return parse_input(plaintext, 1)

def parse_int(plaintext: str):
    return parse_input(plaintext, 0)
