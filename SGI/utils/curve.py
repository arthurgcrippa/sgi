STEPS = 1000

def blending_curve(normalized, curve_type, curve_algorythm):
    lines = []
    assert len(normalized)-1 % 3 != 0
    p1 = normalized[0]
    for i in range(1, len(normalized)):
        if i % 3 == 0:
            p2 = normalized[i]
            partial_lines = curve_segment(p1,r1,r2,p2, curve_type, curve_algorythm)
            p1 = p2
            for line in partial_lines:
                lines.append(line)
        if i % 3 == 1:
            r1 = normalized[i]
        if i % 3 == 2:
            r2 = normalized[i]
    return lines

def b_spline_curve(normalized, curve_type, curve_algorythm):
    lines = []
    if len(normalized) < 4:
        print("Problemas! Não há como formar p1, p2, ")
        print(len(normalized))
    else:
        p0, p1, p2, p3 = normalized[0], normalized[1], normalized[2], normalized[3]
        lines = curve_segment(p0,p1,p2,p3, curve_type, curve_algorythm)
        for i in range(len(normalized)-4):
            p0 = p1
            p1 = p2
            p2 = p3
            p3 = normalized[i+4]
            segment_lines = curve_segment(p0, p1, p2, p3, curve_type, curve_algorythm)
            for line in segment_lines:
                lines.append(line)
    return lines

def curve_segment(p1, p2, p3, p4, curve_type, curve_algorythm):
    lines = []
    if curve_algorythm:
        x1, y1, z1 = polynomial_function(p1, p2, p3, p4, 0, curve_type)
        for i in range(1, STEPS+1):
            t = i/STEPS
            x2, y2, z2 = polynomial_function(p1, p2, p3, p4, t, curve_type)
            lines.append(((x1,y1,z1), (x2,y2,z2)))
            x1, y1, z1 = x2, y2, z2
        return lines
    else:
        return forwarding_differences(STEPS, p1, p2, p3, p4, curve_type)

def polynomial_function(p1, p2, p3, p4, t, curve_type):
    t3, t2 = t**3, t**2
    ax, bx, cx, dx = polynomial_coeficients(p1[0],p2[0],p3[0],p4[0], curve_type)
    ay, by, cy, dy = polynomial_coeficients(p1[1],p2[1],p3[1],p4[1], curve_type)
    az, bz, cz, dz = polynomial_coeficients(p1[2],p2[2],p3[2],p4[2], curve_type)
    x = ax*t3 + bx*t2 + cx*t + dx
    y = ay*t3 + by*t2 + cy*t + dy
    z = az*t3 + bz*t2 + cz*t + dz
    return x,y,z

def bezier(p0, p1, p2, p3, t):
    s = 1-t
    t3, t2 = t**3, t**2
    s3, s2 = s**3, s**2
    x = s3 * p0[0] + 3 * s2 * t * p1[0] + 3 * s * t2 * p2[0] + t3 * p3[0]
    y = s3 * p0[1] + 3 * s2 * t * p1[1] + 3 * s * t2 * p2[1] + t3 * p3[1]
    z = s3 * p0[2] + 3 * s2 * t * p1[2] + 3 * s * t2 * p2[2] + t3 * p3[2]
    return x,y,z

def hermite(p1, r1, r4, p4, t):
    t3, t2 = t**3, t**2
    x = p1[0] * (2*t3 - 3*t2 + 1) + p4[0] * (-2*t3 + 3*t2) + r1[0] * (t3 - 2*t2 + t) + r4[0] * (t3 - t2)
    y = p1[1] * (2*t3 - 3*t2 + 1) + p4[1] * (-2*t3 + 3*t2) + r1[1] * (t3 - 2*t2 + t) + r4[1] * (t3 - t2)
    z = p1[2] * (2*t3 - 3*t2 + 1) + p4[2] * (-2*t3 + 3*t2) + r1[2] * (t3 - 2*t2 + t) + r4[2] * (t3 - t2)
    return x,y,z

def b_spline(p1, p2, p3, p4, t):
    t2, t3 = t**2, t**3
    x = (-t3+3*t2-3*t+1)*p1[0]/6 + (3*t3 -6*t2 + 4)*p2[0]/6 + (-3*t3 + 3*t2 + 3*t + 1)*p3[0]/6 + (t3)*p4[0]/6
    y = (-t3+3*t2-3*t+1)*p1[1]/6 + (3*t3 -6*t2 + 4)*p2[1]/6 + (-3*t3 + 3*t2 + 3*t + 1)*p3[1]/6 + (t3)*p4[1]/6
    z = (-t3+3*t2-3*t+1)*p1[2]/6 + (3*t3 -6*t2 + 4)*p2[2]/6 + (-3*t3 + 3*t2 + 3*t + 1)*p3[2]/6 + (t3)*p4[2]/6
    return x,y,z

def forwarding_differences(n, p1, p2, p3, p4, curve_type):

    ax, bx, cx, dx = polynomial_coeficients(p1[0], p2[0], p3[0], p4[0], curve_type)
    ay, by, cy, dy = polynomial_coeficients(p1[1], p2[1], p3[1], p4[1], curve_type)
    az, bz, cz, dz = polynomial_coeficients(p1[2], p2[2], p3[2], p4[2], curve_type)

    _d, _d2, _d3 = get_delta(n)

    x, y, z = dx, dy, dz
    dx, dy, dz = ax*_d3 + bx*_d2 + cx*_d, ay*_d3 + by*_d2 + cy*_d, az*_d3 + bz*_d2 + cz*_d
    d2x, d2y, d2z = 6*ax*_d3 + 2*bx*_d2, 6*ay*_d3 + 2*by*_d2, 6*az*_d3 + 2*bz*_d2
    d3x, d3y, d3z = 6*ax*_d3, 6*ay*_d3, 6*az*_d3
    lines = []
    x1 = x
    y1 = y
    z1 = z
    for i in range(n):
        x, dx, d2x = x + dx, dx + d2x, d2x + d3x
        y, dy, d2y = y + dy, dy + d2y, d2y + d3y
        z, dz, d2z = z + dz, dz + d2z, d2z + d3z
        x2,y2,z2 = x,y,z
        lines.append(((x1,y1,z1),(x2,y2,z2)))
        x1, y1, z1 = x2, y2, z2
    return lines

def polynomial_coeficients(v1, v2, v3, v4, curve_type):
    if curve_type == 1:
        a = (+2)*v1+(+1)*v2+(+1)*v3+(-2)*v4
        b = (-3)*v1+(-2)*v2+(-1)*v3+(+3)*v4
        c = (+0)*v1+(+1)*v2+(+0)*v3+(+0)*v4
        d = (+1)*v1+(+0)*v2+(+0)*v3+(+0)*v4
        return a, b, c, d
    elif curve_type == 2:
        a = (-1)*v1+(+3)*v2+(-3)*v3+(+1)*v4
        b = (+3)*v1+(-6)*v2+(+3)*v3+(+0)*v4
        c = (-3)*v1+(+3)*v2+(+0)*v3+(+0)*v4
        d = (+1)*v1+(+0)*v2+(+0)*v3+(+0)*v4
        return a, b, c, d
    else:
        a = (-1/6)*v1+(+3/6)*v2+(-3/6)*v3+(+1/6)*v4
        b = (+3/6)*v1+(-6/6)*v2+(+3/6)*v3+(0/6)*v4
        c = (-3/6)*v1+(+0/6)*v2+(+3/6)*v3+(0/6)*v4
        d = (+1/6)*v1+(+4/6)*v2+(+1/6)*v3+(+0/6)*v4
        return a, b, c, d

def get_delta(n):
    _d = 1/n
    _d2, _d3 = _d**2, _d**3
    return _d, _d2, _d3
