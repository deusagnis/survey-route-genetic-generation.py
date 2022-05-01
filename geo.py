import math


def calc_distance(point1, point2):
    return math.sqrt(pow(point1[0] + point2[0], 2) + pow(point1[1] + point2[1], 2))
