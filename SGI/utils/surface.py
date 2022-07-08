from utils import curve
from utils import matrices as mat
import numpy as np

STEPS_T = 10
STEPS_S = 10
ALGO = 1 # Forwarding

def surface(normalized, surface_type):
    lines = []
    matrices = create_matrices(normalized)
    for matrix in matrices:
        matrix_x, matrix_y, matrix_z = matrix[0], matrix[1], matrix[2]
        partial_lines = partial_surface(matrix_x, matrix_y, matrix_z, surface_type)
        for line in partial_lines:
            lines.append(line)
    return lines

def create_matrices(normalized):
    matrices = []
    size = int(np.sqrt(len(normalized)))
    assert size >= 4
    for i in range(int(size/4)):
        matrices.append(create_non_overlapping_matrix(normalized, i))
    if size % 4 != 0:
        matrices.append(create_overlapping_matrix(normalized, size))
    return matrices

def create_overlapping_matrix(normalized, index):
    return create_4x4_matrix(normalized, index, True)

def create_non_overlapping_matrix(normalized, index):
    return create_4x4_matrix(normalized, index, False)

def create_4x4_matrix(normalized, index, OVERLAP):
    matrix_x = []
    matrix_y = []
    matrix_z = []
    size = 4
    first = 0
    if OVERLAP:
        size = index
        first = size-4
    else:
        first += size*index
        size *= index+1
    for i in range(first, size):
        line_x = []
        line_y = []
        line_z = []
        for j in range(first, size):
            line_x.append(normalized[i*size+j][0])
            line_y.append(normalized[i*size+j][1])
            line_z.append(normalized[i*size+j][2])
        matrix_x.append(line_x)
        matrix_y.append(line_y)
        matrix_z.append(line_z)
    return (matrix_x, matrix_y, matrix_z)

def partial_surface(mx, my, mz, surface_type):
    if ALGO:
        return forwarding_surface(mx, my, mz, surface_type)
    else:
        return polynomial_surface(mx, my, mz, surface_type)

def polynomial_surface(mx, my, mz, surface_type):
    combined_matrix_x = get_coeficients(mx, surface_type)
    combined_matrix_y = get_coeficients(my, surface_type)
    combined_matrix_z = get_coeficients(mz, surface_type)
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

def forwarding_surface(mx, my, mz, surface_type):
    mat.show(mx)
    print(mx)
    method_matrix = mat.get_curve(surface_type)
    method_matrix_t = mat.transpose(method_matrix)
    mx = np.dot(method_matrix, np.dot(mx, method_matrix_t))
    my = np.dot(method_matrix, np.dot(my, method_matrix_t))
    mz = np.dot(method_matrix, np.dot(mz, method_matrix_t))
    delta_s, delta_t = 1/STEPS_S, 1/STEPS_T
    ms = mat.get_delta(delta_s)
    mt = mat.get_delta(delta_t)
    mt_t = mat.transpose(mt)
    ddx = np.dot(ms, np.dot(mx, mt_t))
    ddy = np.dot(ms, np.dot(my, mt_t))
    ddz = np.dot(ms, np.dot(mz, mt_t))
    ddx_t, ddy_t, ddz_t = mat.transpose(ddx), mat.transpose(ddy), mat.transpose(ddz)
    lines = []
    for i in range(STEPS_S):
        p1 = (ddx[0][0], ddy[0][0], ddz[0][0])
        p2 = (ddx[0][1], ddy[0][1], ddz[0][1])
        p3 = (ddx[0][2], ddy[0][2], ddz[0][2])
        p4 = (ddx[0][3], ddy[0][3], ddz[0][3])
        for line in curve.forwarding_differences(STEPS_T, p1, p2, p3, p4, surface_type):
            lines.append(line)
        ddx = forward_update(ddx)
        ddy = forward_update(ddy)
        ddz = forward_update(ddz)
    for i in range(STEPS_T):
        p1 = (ddx_t[0][0], ddy_t[0][0], ddz_t[0][0])
        p2 = (ddx_t[0][1], ddy_t[0][1], ddz_t[0][1])
        p3 = (ddx_t[0][2], ddy_t[0][2], ddz_t[0][2])
        p4 = (ddx_t[0][3], ddy_t[0][3], ddz_t[0][3])
        for line in curve.forwarding_differences(STEPS_S, p1, p2, p3, p4, surface_type):
            lines.append(line)
        ddx_t = forward_update(ddx_t)
        ddy_t = forward_update(ddy_t)
        ddz_t = forward_update(ddz_t)
    return lines

def forward_update(matrix):
    r1, r2, r3, r4 = matrix
    r1 = sum(r1, r2)
    r2 = sum(r2, r3)
    r3 = sum(r3, r4)
    return [r1, r2, r3, r4]

def sum(r1, r2):
    r = []
    assert(len(r1) == len(r2))
    for i in range(len(r1)):
        r.append(r1[i]+r2[i])
    return r

def get_coeficients(matrix, type):
    if type == 0:
        return np.dot(matrix, mat.get_bspline())
    if type == 1:
        return np.dot(matrix, mat.get_hermite())
    if type == 2:
        return np.dot(matrix, mat.get_bezier())
