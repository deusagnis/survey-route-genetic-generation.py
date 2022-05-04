import math
import numpy as np
from pyproj import Geod

# Создаём геоид стандарта WGS84.
geod = Geod(ellps="WGS84")


def calc_distance(*points):
    """
    Вычислить геодезическое расстояние вдоль линии, заданной точками.
    """
    points_array = np.array(points)
    return geod.line_length(points_array[:, 1], points_array[:, 0])


def calc_3_points_angle(p1, p2, p3):
    """
    Вычислить величину угла, образованного тремя точками.
    """
    a = calc_distance(p2, p1)
    b = calc_distance(p2, p3)
    c = calc_distance(p1, p3)

    return math.acos((pow(a, 2) + pow(b, 2) - pow(c, 2)) / 2 * a * b)


def gen_borders(area_points):
    """
    Определить прямоугольные границы по точкам.
    """
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


def gen_grid(borders, lat_step, lon_step):
    """
    Создать сетку ключевых точек по заданным границам с заданными шагами по широте и долготе.
    """
    grid = np.array([])
    for lat in np.arange(borders["lat_bot"], borders["lat_top"] + lat_step, lat_step):
        for lon in np.arange(borders["lon_left"], borders["lon_right"] + lon_step, lon_step):
            np.append(grid, [lat, lon])

    return grid
