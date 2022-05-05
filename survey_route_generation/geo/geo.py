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


def calc_rectangle_average_degree_dist(rectangle_borders):
    """
    Вычислить среднюю протяжённость одного градуса по широте и долготе.
    """
    lat_left_height = calc_distance(
        (rectangle_borders["lat_bot"], rectangle_borders["lon_left"]),
        (rectangle_borders["lat_top"], rectangle_borders["lon_left"])
    )
    lat_right_height = calc_distance(
        (rectangle_borders["lat_bot"], rectangle_borders["lon_right"]),
        (rectangle_borders["lat_top"], rectangle_borders["lon_right"])
    )
    lon_bot_width = calc_distance(
        (rectangle_borders["lat_bot"], rectangle_borders["lon_left"]),
        (rectangle_borders["lat_bot"], rectangle_borders["lon_right"])
    )
    lon_top_width = calc_distance(
        (rectangle_borders["lat_top"], rectangle_borders["lon_left"]),
        (rectangle_borders["lat_top"], rectangle_borders["lon_right"])
    )
    average_lat_height = (lat_left_height + lat_right_height) / 2
    average_lon_width = (lon_bot_width + lon_top_width) / 2

    lat_degrees_delta = math.fabs(rectangle_borders["lat_top"] - rectangle_borders["lat_bot"])
    lon_degrees_delta = math.fabs(rectangle_borders["lon_left"] - rectangle_borders["lon_right"])

    return [
        average_lat_height / lat_degrees_delta,
        average_lon_width / lon_degrees_delta
    ]
