"""
Нахождение точки полигона, ближайшей к заданной.
"""
import numpy as np

from survey_route_generation.geo.geo import calc_distance


class PolygonNearestPointToPoint:
    def __init__(self, polygon_vertices, out_point):
        self.polygon_vertices = polygon_vertices
        self.out_point = out_point

    def _calc_vertices_point_distances(self):
        """
        Посчитать расстояния от вершин полигона до заданной точки.
        """
        self._vertices_point_distances = np.array([])

        for point in self.polygon_vertices:
            self._vertices_point_distances = np.append(
                self._vertices_point_distances, calc_distance(point, self.out_point)
            )

    def _find_2_nearest_points(self):
        """
        Найти две вершины полигона, ближайшие к заданной.
        """
        first = None
        second = None
        for point_index in range(self._vertices_point_distances.size):
            point_dist = self._vertices_point_distances[point_index]
            if first is None:
                first = [point_index, point_dist]
                continue

            if point_dist < first[1]:
                second = [*first]
                first = [point_index, point_dist]
            elif second is None or point_dist < second[1]:
                second = [point_index, point_dist]

        self._2_nearest_points = [first, second]

    def _choose_nearest(self):
        """
        Выбрать ближайшую из двух вершин полигона к заданной точке или середину между этими вершинами.
        """
        if self._2_nearest_points[0][1] != self._2_nearest_points[1][1]:
            return self.polygon_vertices[self._2_nearest_points[0][0]]
        else:
            point1 = self.polygon_vertices[self._2_nearest_points[0][0]]
            point2 = self.polygon_vertices[self._2_nearest_points[1][0]]

            return [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]

    def find(self):
        """
        Найти ближайшую точку полигона к заданной.
        """
        self._calc_vertices_point_distances()
        self._find_2_nearest_points()

        return self._choose_nearest()
