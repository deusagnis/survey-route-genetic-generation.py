from survey_route_generation.geo.geo import segments_crossing


class PointInPolygon:
    def __init__(self, polygon):
        self.point = None
        self._point_ray = None
        self.polygon = polygon

    def _gen_point_ray(self):
        return [
            self.point,
            [90, 180]
        ]

    def _calc_crossings(self):
        self._crossing_counter = 0
        for i in range(len(self.polygon)):
            prev_point_index = i - 1 if i > 0 else len(self.polygon) - 1
            prev_point = self.polygon[prev_point_index]
            current_point = self.polygon[i]

            if segments_crossing(prev_point, current_point, self._point_ray[0], self._point_ray[1]):
                self._crossing_counter += 1

    def inside(self, point) -> bool:
        self.point = point
        # выбираем луч
        self._point_ray = self._gen_point_ray()
        # считаем количество пересечений луча и рёбер
        self._calc_crossings()
        # если нечётно то внутри
        return self._crossing_counter % 2 != 0
