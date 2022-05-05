"""
Создание сетки ключевых точек по заданным границам прямоугольной области.
"""
import numpy as np
from survey_route_generation.geo.geo import calc_rectangle_average_degree_dist


class RectangleGridKeypointsGenerator:
    def __init__(self, rectangle_borders, keypoint_distance):
        self.rectangle_borders = rectangle_borders
        self.keypoint_distance = keypoint_distance

    def _calc_grid_steps(self):
        """
        Вычислить шаги для координатной сетки.
        """
        self._lat_step = self.keypoint_distance / self._average_degree_distances[0]
        self._lon_step = self.keypoint_distance / self._average_degree_distances[1]

    def _gen_keypoint_grid(self):
        """
        Сгенерировать сетку ключевых точек.
        """
        grid_keypoints = []
        for lat in np.arange(
                self.rectangle_borders["lat_bot"],
                self.rectangle_borders["lat_top"] + self._lat_step,
                self._lat_step
        ):
            for lon in np.arange(
                    self.rectangle_borders["lon_left"],
                    self.rectangle_borders["lon_right"] + self._lon_step,
                    self._lon_step
            ):
                grid_keypoints.append([lat, lon])

        self._grid_keypoints = np.array(grid_keypoints)

    def _calc_average_degree_distances(self):
        """
        Посчитать среднюю протяжённость градусов по широте и долготе в прямоугольной области.
        """
        self._average_degree_distances = calc_rectangle_average_degree_dist(self.rectangle_borders)

    def gen(self):
        """
        Сгенерировать ключевые точки.
        """
        self._calc_average_degree_distances()
        self._calc_grid_steps()
        self._gen_keypoint_grid()

        return self._grid_keypoints
