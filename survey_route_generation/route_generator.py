"""
Создание и оптимизация маршрута обследования заданной зоны.
"""
import numpy as np
import logging
from survey_route_generation.geo.grid_keyponts_generator import RectangleGridKeypointsGenerator
from survey_route_generation.geo.polygon_nearest_point_to_point import PolygonNearestPointToPoint
from survey_route_generation.geo.geo import gen_borders
from shapely.geometry import Point, Polygon


class RouteGenerator:
    def __init__(self, genetic_optimal_route_finder):
        self.genetic_optimal_route_finder = genetic_optimal_route_finder

        self.vehicle_data = None
        self.mission_settings = None
        self.survey_area_points = None

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

        logging.info("Количество ключевых точек в маршруте: \t" + str(self._inside_grid_key_points.shape[0]))

    def _gen_keypoint_grid(self):
        """
        Сгенерировать сетку ключевых точек зоны обследования.
        """
        generator = RectangleGridKeypointsGenerator(self._area_borders, self._keypoint_distance)
        self._grid_keypoints = generator.gen()
        logging.info("Количество ключевых точек в начальной сетке: \t" + str(self._grid_keypoints.shape[0]))

    def _calc_keypoint_distance(self):
        """
        Вычислить расстояние между ключевыми точками.
        """
        self._keypoint_distance = self.vehicle_data.vision_width * (1 - 0.05)
        logging.info("Расстояние между парой ключевых точек: \t" + str(self._keypoint_distance))

    def _gen_area_borders(self):
        self._area_borders = gen_borders(self.survey_area_points)
        logging.info("Границы описанного прямоугольника зоны обследования: \t" + str(self._area_borders))

    def _choose_in_point(self):
        """
        Выбрать точку влёта в зону обследования.
        """
        p = PolygonNearestPointToPoint(self.survey_area_points, self.mission_settings.start_point)
        self._area_in_point = p.find()
        logging.info("Точка входа в зону обследования: \t" + str(self._area_in_point))

    def _choose_out_point(self):
        """
        Выбрать точку вылета из зоны обследования.
        """
        p = PolygonNearestPointToPoint(self.survey_area_points, self.mission_settings.end_point)
        self._area_out_point = p.find()
        logging.info("Точка выхода из зоны обследования: \t" + str(self._area_out_point))

    def _find_optimal_route(self):
        """
        Найти оптимальный маршрут обследования.
        """
        self.optimal_route = self.genetic_optimal_route_finder.find(
            self._inside_grid_key_points,
            self._area_in_point,
            self._area_out_point,
            self._keypoint_distance
        )
        self.route_fitness = self.genetic_optimal_route_finder.best_genotype_fitness
        self.route_hash = self.genetic_optimal_route_finder.best_genotype_hash

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

    def generate_route(self, vehicle_data, mission_settings, survey_area_points):
        """
        Составить маршрут обследования зоны.
        """
        self.vehicle_data = vehicle_data
        self.mission_settings = mission_settings
        self.survey_area_points = survey_area_points

        self._choose_in_out_points()
        self._gen_keypoints()
        self._find_optimal_route()

        return {
            "in_point": self._area_in_point,
            "route": self.optimal_route,
            "route_fitness": self.route_fitness,
            "route_hash": self.route_hash,
            "out_point": self._area_out_point
        }
