import math
import numpy as np


def calc_distance(point1, point2):
    return math.sqrt(pow(point1[0] + point2[0], 2) + pow(point1[1] + point2[1], 2))


def segments_crossing(p00, p01, p10, p11, eps=0.000000001):
    m1 = np.cross(
        [p11[0] - p10[0], p11[1] - p10[1]],
        [p00[0] - p10[0], p00[1] - p10[1]]
    )[0]
    m2 = np.cross(
        [p11[0] - p10[0], p11[1] - p10[1]],
        [p01[0] - p10[0], p01[1] - p10[1]]
    )[0]
    m3 = np.cross(
        [p01[0] - p00[0], p01[1] - p00[1]],
        [p10[0] - p00[0], p10[1] - p00[1]]
    )[0]
    m4 = np.cross(
        [p01[0] - p00[0], p01[1] - p00[1]],
        [p11[0] - p00[0], p11[1] - p00[1]]
    )[0]

    if m1 * m2 < eps and m3 * m4 < eps:
        return True

    return False


def calc_3_points_angle(p1, p2, p3):
    a = calc_distance(p2, p1)
    b = calc_distance(p2, p3)
    c = calc_distance(p1, p3)

    return math.acos((pow(a, 2) + pow(b, 2) - pow(c, 2)) / 2 * a * b)


def gen_borders(area_points):
    lat_bot = None
    lat_top = None
    lon_left = None
    lon_right = None

    for point in area_points:
        if lat_bot is None or point[0] < lat_bot:
            lat_bot = point[0]
        if lat_top is None or point[0] > lat_top:
            lat_top = point[0]
        if lon_left is None or point[1] < lon_left:
            lon_left = point[1]
        if lon_right is None or point[1] > lon_right:
            lon_right = point[1]

    return {
        "lat_bot": lat_bot,
        "lat_top": lat_top,
        "lon_left": lon_left,
        "lon_right": lon_right
    }
