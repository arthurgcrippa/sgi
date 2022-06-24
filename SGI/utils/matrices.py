import numpy as np
import math
import sys
def translation(point, matrix):
    x,y,z = point[0], point[1], point[2]
    trans = [[1,0,0,0],
             [0,1,0,0],
             [0,0,1,0],
             [x,y,z,1]]
    return np.dot(matrix, trans)

def scaling(scale, center, matrix):
    dx, dy, dz = scale[0], scale[1], scale[2]
    scale_matrix = [[dy,0,0,0],
                    [0,dy,0,0],
                    [0,0,dz,0],
                    [0,0,0,1]]
    x, y, z = center[0], center[1], center[2]
    matrix = translation((-x,-y,-z), matrix)
    matrix = np.dot(matrix, scale_matrix)
    return translation((x,y,z),matrix)

def rotation_x(theta, matrix):
    sin, cos = np.sin(math.radians(theta)), np.cos(math.radians(theta))
    matrix_rotation_x = [[1,   0,    0,    0],
                         [0,  cos,  sin,   0],
                         [0, -sin,  cos,   0],
                         [0,   0,    0,    1]]
    return np.dot(matrix, matrix_rotation_x)

def rotation_y(theta, matrix):
    sin, cos = np.sin(math.radians(theta)), np.cos(math.radians(theta))
    matrix_rotation_y = [[cos, 0, -sin, 0],
                         [0,   1,   0,  0],
                         [sin, 0,  cos,  0],
                         [0,   0,   0,  1]]
    return np.dot(matrix, matrix_rotation_y)

def rotation_z(theta, matrix):
    sin, cos = np.sin(math.radians(theta)), np.cos(math.radians(theta))
    matrix_rotation_z = [[cos, sin,   0,  0],
                         [-sin, cos,  0,  0],
                         [0,     0,   1,  0],
                         [0,     0,   0,  1]]
    return np.dot(matrix, matrix_rotation_z)

def project(d, matrix):
    matrix_projection = [[1, 0, 0,   0],
                         [0, 1, 0,   0],
                         [0, 0, 1, 1/d],
                         [0, 0, 0,   1]]
    return np.dot(matrix_projection, matrix)

def project2(d, matrix):
    matrix_projection = [[1, 0, 0,   0],
                         [0, 1, 0,   0],
                         [0, 0, 1, 1/d],
                         [0, 0, 0,   0]]
    return np.dot(matrix_projection, matrix)

def identity():
    matrix = [[1,0,0,0],
              [0,1,0,0],
              [0,0,1,0],
              [0,0,0,1]]
    return matrix

def equals(m1, m2): #EQUALS
    if len(m1) != len(m2):
        return False
    for i in range(len(m1)):
        if len(m1[i]) != len(m2[i]):
            return False
        for j in range(len(m1[i])):
            if round(m1[i][j],2) != round(m2[i][j],2):
                return False
    return True

def show(matrix):
    print("###################")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            sys.stdout.write("{:.2f}".format(matrix[i][j])+"  ")
        print()

def degree(p1, p2, p3):
    if p1 == p2:
        return 0
    hipo = dist(p1,p2)
    cat_op = dist(p2,p3)
    cat_ad = dist(p1, p3)
    sin = cat_op/hipo
    cos = cat_ad/hipo
    quad = 0
    degree = np.degrees(np.arcsin(sin))
    x, y = p3[0], p3[1]
    if x < 0 and y < 0: #3rd
        degree = 180 + degree
    elif x<0 and y>=0: #2nd
        degree = 180 - degree
    elif x>=0 and y < 0: #4th
        degree = 360 + degree
    return degree

def dist(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
