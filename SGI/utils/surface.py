from utils import curve
import numpy as np

STEPS_T = 10
STEPS_S = 10
def blending_surface(normalized, surface_type):
    p = normalized
    matrix_x = [[p[0][0],  p[1][0],  p[2][0],  p[3][0]],
                [p[4][0],  p[5][0],  p[6][0],  p[7][0]],
                [p[8][0],  p[9][0],  p[10][0], p[11][0]],
                [p[12][0], p[13][0], p[14][0], p[15][0]]]

    matrix_y = [[p[0][1],  p[1][1],  p[2][1],  p[3][1]],
                [p[4][1],  p[5][1],  p[6][1],  p[7][1]],
                [p[8][1],  p[9][1],  p[10][1], p[11][1]],
                [p[12][1], p[13][1], p[14][1], p[15][1]]]

    matrix_z = [[p[0][2],  p[1][2],  p[2][2],  p[3][2]],
                [p[4][2],  p[5][2],  p[6][2],  p[7][2]],
                [p[8][2],  p[9][2],  p[10][2], p[11][2]],
                [p[12][2], p[13][2], p[14][2], p[15][2]]]

    combined_matrix_x = get_coeficients(matrix_x, surface_type)
    combined_matrix_y = get_coeficients(matrix_y, surface_type)
    combined_matrix_z = get_coeficients(matrix_z, surface_type)
    lines = []
    s_list = []
    t_list = []
    for i in range(STEPS_S):
        s = i/STEPS_S
        matrix_s = [s**3, s**2, s, 1]
        s_list.append(matrix_s)
    for j in range(STEPS_T):
        t = j/STEPS_T
        matrix_t = [t**3, t**2, t, 1]
        t_list.append(matrix_t)

    for i in range(len(s_list)):
        x1 = np.dot([0,0,0,1], np.dot(s_list[i], combined_matrix_x))
        y1 = np.dot([0,0,0,1], np.dot(s_list[i], combined_matrix_y))
        z1 = np.dot([0,0,0,1], np.dot(s_list[i], combined_matrix_z))
        for j in range(len(t_list)):
            x2 = np.dot(t_list[j], np.dot(s_list[i], combined_matrix_x))
            y2 = np.dot(t_list[j], np.dot(s_list[i], combined_matrix_y))
            z2 = np.dot(t_list[j], np.dot(s_list[i], combined_matrix_z))
            lines.append([(x1,y1,z1),(x2,y2,z2)])
            x1, y1, z1 = x2, y2, z2

    for i in range(len(t_list)):
        x1 = np.dot(t_list[i], np.dot([0,0,0,1], combined_matrix_x))
        y1 = np.dot(t_list[i], np.dot([0,0,0,1], combined_matrix_y))
        z1 = np.dot(t_list[i], np.dot([0,0,0,1], combined_matrix_z))
        for j in range(len(s_list)):
            x2 = np.dot(t_list[i], np.dot(s_list[j], combined_matrix_x))
            y2 = np.dot(t_list[i], np.dot(s_list[j], combined_matrix_y))
            z2 = np.dot(t_list[i], np.dot(s_list[j], combined_matrix_z))
            lines.append([(x1,y1,z1),(x2,y2,z2)])
            x1, y1, z1 = x2, y2, z2
    return lines

def get_coeficients(matrix, type):
    if type == 1:
        return get_hermite_coeficients(matrix)
    if type == 2:
        return get_bezier_coeficients(matrix)

def get_bezier_coeficients(matrix):
    matrix_bezier = [[-1,  3, -3, 1],
                     [ 3, -6,  3, 0],
                     [-3,  3,  0, 0],
                     [ 1,  0,  0, 0]]
    return np.dot(matrix, matrix_bezier)

def get_hermite_coeficients(matrix):
    matrix_hermite = [[-2,  -3,  0, 1],
                      [ 1,  -2,  1, 0],
                      [ 1,  -1,  0, 0],
                      [-2,   3,  0, 0]]
    return np.dot(matrix, matrix_hermite)
