from survey_route_generation.geo.polygon_nearest_point import PolygonNearestPoint
from survey_route_generation.geo.grid_keyponts_generator import GridKeypointsGenerator
from survey_route_generation.geo.geo import calc_distance, gen_borders
from survey_route_generation.geo.point_in_polygon import PointInPolygon
from survey_route_generation.genetic.genetic_optimal_route_finder import GeneticOptimalRouteFinder


class RouteGenerator:
    def __init__(self, vehicle_data, way_settings, survey_area_points):
        self.vehicle_data = vehicle_data
        self.way_settings = way_settings
        self.survey_area_points = survey_area_points

    def _calc_grid_steps(self):
        return [
            self._keypoint_distance / self._average_degree_distances[0],
            self._keypoint_distance / self._average_degree_distances[1],
        ]

    def _calc_keypoint_distance(self):
        return self.vehicle_data["vision_width"] * (1 - 0.05)

    def _calc_average_degree_dist(self):
        lat_left_height = calc_distance(
            (self._area_borders["lat_bot"], self._area_borders["lon_left"]),
            (self._area_borders["lat_top"], self._area_borders["lon_left"])
        )
        lat_right_height = calc_distance(
            (self._area_borders["lat_bot"], self._area_borders["lon_right"]),
            (self._area_borders["lat_top"], self._area_borders["lon_right"])
        )
        lon_bot_width = calc_distance(
            (self._area_borders["lat_bot"], self._area_borders["lon_left"]),
            (self._area_borders["lat_bot"], self._area_borders["lon_right"])
        )
        lon_top_width = calc_distance(
            (self._area_borders["lat_top"], self._area_borders["lon_left"]),
            (self._area_borders["lat_top"], self._area_borders["lon_right"])
        )
        average_lat_height = (lat_left_height + lat_right_height) / 2
        average_lon_width = (lon_bot_width + lon_top_width) / 2

        lat_degrees_delta = self._area_borders["lat_top"] - self._area_borders["lat_bot"]
        lon_degrees_delta = self._area_borders["lon_left"] - self._area_borders["lon_right"]

        return [
            average_lat_height / lat_degrees_delta,
            average_lon_width / lon_degrees_delta
        ]

    def _choose_in_point(self):
        self._area_in_point = PolygonNearestPoint(self.survey_area_points, self.way_settings.start_point)

    def _choose_out_point(self):
        self._area_out_point = PolygonNearestPoint(self.survey_area_points, self.way_settings.end_point)

    def _choose_in_out_points(self):
        # выбрать точку влёта в область
        self._choose_in_point()
        # выбрать точку вылета из области
        self._choose_out_point()

    def _gen_keypoint_grid(self):
        # узнаём среднюю протяжённость 1 градуса для широты и долготы
        self._area_borders = gen_borders(self.survey_area_points)
        self._average_degree_distances = self._calc_average_degree_dist()
        # вычисляем расстояние между узлами
        self._keypoint_distance = self._calc_keypoint_distance()
        # вычисляем приращение в градусах по широте и долготе
        self._grid_steps = self._calc_grid_steps()
        # заполняем полигон узлами
        generator = GridKeypointsGenerator(self._area_borders, self._grid_steps[0], self._grid_steps[1])
        self._grid_keypoints = generator.gen()

    def _filter_keypoints(self):
        self._inside_grid_key_points = []
        # убираем точки, не лежащие внутри полигона
        checker = PointInPolygon(self.survey_area_points)

        for key_point in self._grid_keypoints:
            if checker.inside(key_point):
                self._inside_grid_key_points.append(key_point)

    def _find_optimal_route(self):
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
        self._choose_in_out_points()
        self._gen_keypoint_grid()

        return self._find_optimal_route()
