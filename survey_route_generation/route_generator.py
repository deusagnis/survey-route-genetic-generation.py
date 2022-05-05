"""
Создание и оптимизация маршрута обследования заданной зоны.
"""
import numpy as np

from survey_route_generation.geo.grid_keyponts_generator import RectangleGridKeypointsGenerator
from survey_route_generation.geo.polygon_nearest_point_to_point import PolygonNearestPointToPoint
from survey_route_generation.geo.geo import gen_borders
from survey_route_generation.genetic.genetic_optimal_route_finder import GeneticOptimalRouteFinder
from shapely.geometry import Point, Polygon


class RouteGenerator:
    def __init__(self, vehicle_data, way_settings, survey_area_points):
        self.vehicle_data = vehicle_data
        self.way_settings = way_settings
        self.survey_area_points = survey_area_points

    def _filter_keypoints(self):
        """
        Отфильтровать ключевые точки, оставив только точки, доступные для полёта.
        """
        polygon = Polygon(self.survey_area_points)

        inside_points = []
        for key_point in self._grid_keypoints:
            point = Point(key_point[0], key_point[1])
            if polygon.contains(point):
                inside_points.append(key_point)

        self._inside_grid_key_points = np.array(inside_points)
        print("Количество ключевых точек в маршруте:", self._inside_grid_key_points.shape[0])

    def _gen_keypoint_grid(self):
        """
        Сгенерировать сетку ключевых точек зоны обследования.
        """
        generator = RectangleGridKeypointsGenerator(self._area_borders, self._keypoint_distance)
        self._grid_keypoints = generator.gen()
        print("Количество ключевых точек в начальной сетке:", self._grid_keypoints.shape[0])

    def _calc_keypoint_distance(self):
        """
        Вычислить расстояние между ключевыми точками.
        """
        self._keypoint_distance = self.vehicle_data.vision_width * (1 - 0.05)
        print("Расстояние между парой ключевых точек:", self._keypoint_distance)

    def _gen_area_borders(self):
        self._area_borders = gen_borders(self.survey_area_points)
        print("Границы описанного прямоугольника зоны обследования:", self._area_borders)

    def _choose_in_point(self):
        """
        Выбрать точку влёта в зону обследования.
        """
        p = PolygonNearestPointToPoint(self.survey_area_points, self.way_settings.start_point)
        self._area_in_point = p.find()
        print("Точка входа в зону обследования:", self._area_in_point)

    def _choose_out_point(self):
        """
        Выбрать точку вылета из зоны обследования.
        """
        p = PolygonNearestPointToPoint(self.survey_area_points, self.way_settings.end_point)
        self._area_out_point = p.find()
        print("Точка выхода из зоны обследования:", self._area_out_point)

    def _find_optimal_route(self):
        """
        Найти оптимальный маршрут обследования.
        """
        finder = GeneticOptimalRouteFinder(
            self._inside_grid_key_points,
            self._area_in_point,
            self._area_out_point,
            0.2,
            "percent",
            2,
            1.5
        )

        self.optimal_route = finder.find()

    def _gen_keypoints(self):
        """
        Сгенерировать ключевые точки маршрута, покрывающие область обследования.
        """
        self._gen_area_borders()
        self._calc_keypoint_distance()
        self._gen_keypoint_grid()
        self._filter_keypoints()

    def _choose_in_out_points(self):
        """
        Выбрать точки влёта и вылета из зоны обследования.
        """
        self._choose_in_point()
        self._choose_out_point()

    def generate_route(self):
        """
        Составить маршрут обследования зоны поиска.
        """
        self._choose_in_out_points()
        self._gen_keypoints()
        self._find_optimal_route()

        return self.optimal_route
