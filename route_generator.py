class RouteGenerator:
    def __init__(self, vehicle_data, way_settings, survey_area_points):
        self.vehicle_data = vehicle_data
        self.way_settings = way_settings
        self.survey_area_points = survey_area_points

    def _choose_in_out_points(self):
        pass

    def _gen_keypoint_grid(self):
        pass

    def _find_optimal_route(self):
        pass

    def generate_route(self):
        self._choose_in_out_points()
        self._gen_keypoint_grid()
        self._find_optimal_route()
