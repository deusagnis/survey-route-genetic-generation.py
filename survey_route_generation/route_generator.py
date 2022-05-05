"""
Создание и оптимизация маршрута обследования заданной зоны.
"""
import numpy as np

from survey_route_generation.geo.polygon_nearest_point_to_point import PolygonNearestPointToPoint
from survey_route_generation.geo.geo import calc_rectangle_average_degree_dist, gen_borders, gen_grid
from survey_route_generation.genetic.genetic_optimal_route_finder import GeneticOptimalRouteFinder
from shapely.geometry import Point, Polygon


class RouteGenerator:
    def __init__(self, vehicle_data, way_settings, survey_area_points):
        self.vehicle_data = vehicle_data
        self.way_settings = way_settings
        self.survey_area_points = survey_area_points

    def _calc_grid_steps(self):
        """
        Вычислить шаги для координатной сетки.
        """
        self._grid_steps = [
            self._keypoint_distance / self._average_degree_distances[0],
            self._keypoint_distance / self._average_degree_distances[1],
        ]

    def _calc_keypoint_distance(self):
        """
        Вычислить расстояние между ключевыми точками.
        """
        self._keypoint_distance = self.vehicle_data["vision_width"] * (1 - 0.05)

    def _choose_in_point(self):
        """
        Выбрать точку влёта в зону обследования.
        """
        self._area_in_point = PolygonNearestPointToPoint(self.survey_area_points, self.way_settings.start_point)

    def _choose_out_point(self):
        """
        Выбрать точку вылета из зоны обследования.
        """
        self._area_out_point = PolygonNearestPointToPoint(self.survey_area_points, self.way_settings.end_point)

    def _choose_in_out_points(self):
        """
        Выбрать точки влёта и вылета из зоны обследования.
        """
        self._choose_in_point()
        self._choose_out_point()

    def _gen_keypoint_grid(self):
        self._grid_keypoints = gen_grid(self._area_borders, self._grid_steps[0], self._grid_steps[1])

    def _calc_average_degree_distances(self):
        self._average_degree_distances = calc_rectangle_average_degree_dist(self._area_borders)

    def _gen_area_borders(self):
        self._area_borders = gen_borders(self.survey_area_points)

    def _gen_keypoints(self):
        """
        Сгенерировать сетку ключевых точек, покрывающую область обследования.
        """
        self._gen_area_borders()
        self._calc_average_degree_distances()
        self._calc_keypoint_distance()
        self._calc_grid_steps()
        self._gen_keypoint_grid()

    def _filter_keypoints(self):
        """
        Отфильтровать ключевые точки, оставив только точки, доступные для полёта.
        """
        self._inside_grid_key_points = np.array([])
        polygon = Polygon(self.survey_area_points)

        for key_point in self._grid_keypoints:
            point = Point(key_point[0], key_point[1])
            if polygon.contains(point):
                self._inside_grid_key_points = np.append(self._inside_grid_key_points, key_point)

    def _find_optimal_route(self):
        """
        Найти оптимальный маршрут обследования.
        """
        finder = GeneticOptimalRouteFinder(
            self._grid_keypoints,
            self._area_in_point,
            self._area_out_point,
            0.2,
            "percent",
            2,
            1.5
        )

        return finder.find()

    def generate_route(self):
        """
        Составить маршрут обследования зоны поиска.
        """
        self._choose_in_out_points()
        self._gen_keypoints()

        return self._find_optimal_route()
