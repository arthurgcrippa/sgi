
SYMBOLS = ["(" , ")" , "," , ";" , ".", "-"]
NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
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

def malformed_input(plaintext: str, error_message):
    for char in plaintext:
        if char not in set(SYMBOLS).union(NUMBERS): #1 INPUT CAN ONLY CONTAIN NUMBERS AND RESERVED SYMBOLS
            error_message.append(get_error_message(1))
            return True
    size = len(plaintext)
    if size == 0:
        error_message.append(get_error_message(2))
        return True
    if plaintext[0] != "(": #STARTS WITH OPENING BRACKET
        error_message.append(get_error_message(3))
        return True
    if plaintext[size-1] != ")": #ENDS WITH CLOSING BRACKET
        error_message.append(get_error_message(4))
        return True
    for i in range(size):
        c1 = plaintext[i]
        if i+1 < size:
            c2 = plaintext[i+1]
            if c1 in SYMBOLS and c1 == c2: #CANNOT REPEAT NON-NUMERIC CHARACTERS
                error_message.append(get_error_message(5))
                return True
            if c1 == ")" and c2 != ";": #CLOSING BRACKET ")" FOLLOWS ";" COORDINATE SEPARATOR
                error_message.append(get_error_message(6))
                return True
            if c1 == ";" and c2 != "(": #COORDINATE SEPARATOR ";" PRECEDES "(" OPENING BRACKET
                error_message.append(get_error_message(7))
                return True
            if c1 in SYMBOLS and c2 in ["." , ","]: #NUM SEPARATOR AND FP MARKER FOLLOW NUMERIC CHAR
                error_message.append(get_error_message(8))
                return True
            if c1 in ["." , "-"] and c2 in SYMBOLS: #NUM SEP, FP MARK AND NEG SYMBOL BEFORE NUM
                error_message.append(get_error_message(9))
                return True
            if c1 == ',' and c2 in SYMBOLS and c2 != "-":
                error_message.append(get_error_message(10))
                return True
            if c1 not in ["(" , ","] and c2 == "-": #NEG SYMBOL FOLLOWS OP BRECK OR NUM SEPARATOR
                error_message.append(get_error_message(11))
                return True
            if c1 in NUMBERS and c2 in ["(", ";"]: #CANNOT HAVE NUMBERS OUTSIDE BRACKETS
                error_message.append(get_error_message(12))
                return True
            if c1 in [")",";"] and c2 in NUMBERS: #CANNOT HAVE NUMBERS OUTISDE BRACKETS
                error_message.append(get_error_message(13))
                return True

    lenghts = []
    for coordinate in plaintext.split(";"):
        coordinate = coordinate.replace("(", "").replace(")", "")
        xyz = coordinate.split(",")
        for value in xyz:
            try:
                float(value)
            except:
                error_message.append(get_error_message(14))
                return True
        length = len(xyz)
        if length != 2 and length != 3:
            error_message.append(get_error_message(15))
            return True
        lenghts.append(length)
    return len(set(lenghts)) != 1

def get_error_message(error_code: int):
    if error_code == 1:
        return "O valor inserido contém caractéres inválidos, tente novamente"
    elif error_code == 2:
        return "Você não inseriu nenhum valor :|"
    elif error_code == 3:
        return "Não esqueça de colocar parênteses ( ) ao redor de cada coordenada"
    elif error_code == 4:
        return "Não esqueça de colocar parênteses ( ) ao redor de cada coordenada"
    elif error_code == 5:
        return "Certeza que não reperiu nenhum caractére? Lembre que NÃO aceitamos parenteses duplos (())"
    elif error_code == 6:
        return "Sempre use ';' para separar dois pares de cordenadas, Não estás usando ',' por acaso?"
    elif error_code == 7:
        return "Somente use ';' para separar dois pares cordenadas. Assim: (p1);(p2)"
    elif error_code == 8:
        return "Utilize a virgula ',' para separar as coordenadas x, y e z dentro da tupla: (x,y,z)"
    elif error_code == 9:
        return "Cuidado com sinais e pontos. Use somente entre números"
    elif error_code == 10:
        return "Cuidado com a virgula. Use somente entre números"
    elif error_code == 11:
        return "Pode ser tentador, mas não ponha o sinal de negativo fora do parenteses, siga o exemplo: (-x,-y,-z)"
    elif error_code == 12:
        return "A cordenada fugiu!!! Não deixe nenhum número fora dos parenteses, traga-o de volta"
    elif error_code == 13:
        return "A cordenada fugiu!!! Não deixe nenhum número fora dos parenteses, traga-o de volta"
    elif error_code == 14:
        return "Eu não sei o que é isso aqui, mas claramente não é um float, tente um número da próxima vez"
    elif error_code == 15:
        return "As coordenadas possuem tamanhos diferentes. Deixe sempre com as mesmas dimensões. 2D: (x1,y1);(x2,y2)  3D: (x1,y1,z1);(x2,y2,z2)"
    else:
        return "unidentified error"

def parse_float(plaintext: str):
    return parse_input(plaintext, 1)

def parse_int(plaintext: str):
    return parse_input(plaintext, 0)
