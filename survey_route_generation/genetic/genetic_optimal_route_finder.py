"""
Применение генетического алгоритма для поиска оптимальной комбинации путевых точек - маршрута.
"""
import math
import random
from shapely.geometry import LineString
import numpy as np

from survey_route_generation.geo.geo import calc_distance, calc_3_points_angle


class GeneticOptimalRouteFinder:
    def __init__(self,
                 genetic_algo,
                 mutation_swap_value=0.2,
                 mutation_swap_type="percent",
                 route_distance_weight=2,
                 route_turns_angle_weight=1.5,
                 route_self_intersection_weight=2
                 ):
        """
        :param genetic_algo: Генетический алгоритм.
        :param mutation_swap_value: Значение количества мутаций в генотипе.
        :param mutation_swap_type: Тип значения количества мутаций: точное число или процент от длины генотипа.
        :param route_distance_weight: Вес значимости сокращения длины маршрута для функции оценки приспособленности.
        :param route_turns_angle_weight: Вес значимости плавности маршрута для функции оценки приспособленности.
        :param route_self_intersection_weight: Вес значимости самопересечений для функции оценки приспособленности.
        """
        self.genetic_algo = genetic_algo
        self.mutation_swap_value = mutation_swap_value
        self.mutation_swap_type = mutation_swap_type
        self.route_distance_weight = route_distance_weight
        self.route_turns_angle_weight = route_turns_angle_weight
        self.route_self_intersection_weight = route_self_intersection_weight

        self.route_points = None
        self.in_point = None
        self.out_point = None

    def _calc_route_fitness(self):
        """
        Посчитать значение функции приспособленности.
        """
        return (self._normalized_route_turns_angle * self.route_turns_angle_weight -
                self._normalized_route_distance * self.route_distance_weight -
                self._normalized_route_self_interactions * self.route_self_intersection_weight +
                self.route_distance_weight + self.route_turns_angle_weight + self.route_self_intersection_weight
                )

    def _normalize_route_self_interactions(self):
        """
        Нормализовать значение количества самопересечений маршрута.
        """
        self._normalized_route_self_interactions = self._route_self_interactions / self._max_route_self_restrictions

    def _normalize_route_turns_angle(self):
        """
        Нормализовать значение размера поворотов маршрута.
        """
        self._normalized_route_turns_angle = self._route_turns_angle / self._max_route_turns_angle

    def _normalize_route_distance(self):
        """
        Нормализовать значение длины маршрута.
        """
        self._normalized_route_distance = self._route_distance / self._max_route_distance

    def _add_route_angles(self, route):
        """
        Добавить к значению размера поворотов маршрута повороты между точками маршрута.
        """
        for i in range(route.shape[0] - 2):
            point = self._get_gen_point(route[i])
            next_point = self._get_gen_point(route[i + 1])
            after_next_point = self._get_gen_point(route[i + 2])

            self._route_turns_angle += calc_3_points_angle(point, next_point, after_next_point)

    def _add_start_end_angles(self, route):
        """
        Добавить к значению размера поворотов маршрута повороты между точкой входа и точкой выхода.
        """
        first_point = self._get_gen_point(route[0])
        second_point = self._get_gen_point(route[1])
        last_point = self._get_gen_point(route.shape[0] - 1)
        pre_last_point = self._get_gen_point(route.shape[0] - 2)

        self._route_turns_angle += calc_3_points_angle(self.in_point, first_point, second_point)
        self._route_turns_angle += calc_3_points_angle(pre_last_point, last_point, self.out_point)

    def _add_route_distance(self, route):
        """
        Добавить к значению длины маршрута расстояния между точками маршрута.
        """
        for i in range(route.shape[0] - 1):
            point = self._get_gen_point(route[i])
            next_point = self._get_gen_point(route[i + 1])

            self._route_distance += calc_distance(point, next_point)

    def _add_start_end_distances(self, route):
        """
        Добавить к значению длины маршрута расстояния между точками входа и выхода.
        """
        first_point = self._get_gen_point(route[0])
        last_point = self._get_gen_point(route.shape[0] - 1)

        self._route_distance += calc_distance(self.in_point, first_point)
        self._route_distance += calc_distance(last_point, self.out_point)

    def _calc_route_self_intersection(self, route):
        """
        Посчитать количество само-пересечений.
        """
        self._route_self_interactions = 0
        for i in range(route.shape[0] - 1):
            point1 = self._get_gen_point(route[i])
            point2 = self._get_gen_point(route[i + 1])
            line1 = LineString([point1, point2])
            for j in range(i, route.shape[0] - 1):
                point3 = self._get_gen_point(route[j])
                point4 = self._get_gen_point(route[j])
                line2 = LineString([point3, point4])
                if line1.crosses(line2):
                    self._route_self_interactions += 1

    def _calc_route_turns_angle(self, route):
        """
        Посчитать сумму углов поворотов маршрута.
        """
        self._route_turns_angle = 0
        self._add_start_end_angles(route)
        self._add_route_angles(route)

    def _calc_route_distance(self, route):
        """
        Посчитать суммарное расстояние маршрута.
        """
        self._route_distance = 0
        self._add_start_end_distances(route)
        self._add_route_distance(route)

    def _route_fitness(self, route):
        """
        Посчитать приспособленность маршрута.
        """
        self._calc_route_distance(route)
        self._calc_route_turns_angle(route)
        self._calc_route_self_intersection(route)

        self._normalize_route_distance()
        self._normalize_route_turns_angle()
        self._normalize_route_self_interactions()

        return self._calc_route_fitness()

    def _cross_routes(self, route_group):
        """
        Скрестить несколько маршрутов в один.
        """
        points_usage = np.full(self.route_points.shape[0], False)

        child_genotype = []
        for i in range(self.route_points.shape[0]):
            for genotype in route_group:
                point_index = genotype[i]
                if not points_usage[point_index]:
                    child_genotype.append(point_index)
                    points_usage[point_index] = True

        return np.array(child_genotype)

    def _calc_genotype_positions_weight(self, genotype):
        """
        Вычислить позиционный вес генотипа.
        """
        weight = 0
        pos_index = 0
        for point_index in genotype:
            weight += pos_index * point_index
            pos_index += 1

        return weight

    def _mutate_route(self, route):
        """
        Мутировать маршрут путём случайных перестановок в порядке следования.
        """
        for i in range(self._mutation_swap_count):
            index1 = random.randint(0, self.route_points.shape[0] - 1)
            index2 = random.randint(0, self.route_points.shape[0] - 1)
            temp = route[index1]
            route[index1] = route[index2]
            route[index2] = temp

        return route

    def _genotype_to_route(self, genotype):
        """
        Собрать маршрут по генотипу.
        """
        route = []
        for gen in genotype:
            route.append(self._get_gen_point(gen))

        return np.array(route)

    def _find_best_genotype(self):
        """
        Подобрать оптимальный маршрут.
        """
        self._best_genotype = self.genetic_algo.find_best_genotype(
            self._points_genome,
            self._route_fitness,
            self._calc_genotype_positions_weight,
            self._cross_routes,
            self._mutate_route,
        )

    def _calc_route_max_self_intersections(self):
        """
        Посчитать максимальную величину количества самопересечений маршрута.
        """
        self._max_route_self_restrictions = 2 * self.route_points.shape[0]

    def _calc_route_max_turns_angle(self):
        """
        Посчитать максимальную величину суммы углов маршрута.
        """
        self._max_route_turns_angle = 3.14 * self.route_points.shape[0]

    def _calc_route_max_distance(self):
        """
        Посчитать максимальную величину расстояния маршрута.
        """
        self._max_route_distance = calc_distance(
            self.route_points[0],
            self.route_points[self.route_points.shape[0] - 1]
        ) * self.route_points.shape[0] * 10

    def _count_mutation_swaps(self):
        """
        Посчитать количество перестановок в маршруте при мутации.
        """
        if self.mutation_swap_type == "percent":
            self._mutation_swap_count = math.floor(self.route_points.shape[0] * self.mutation_swap_value)
        else:
            self._mutation_swap_count = self.mutation_swap_value

    def _get_gen_point(self, gen):
        """
        Получить точку маршрута по её "гену".
        """
        return self.route_points[gen]

    def _create_points_genome(self):
        """
        Создать генотип для точек маршрута.
        """
        self._points_genome = np.arange(self.route_points.shape[0])

    def find(self,
             route_points,
             in_point,
             out_point
             ):
        """
        Найти оптимальный маршрут.

        :param route_points: Точки маршрута, которые надо посетить.
        :param in_point: Точка входа в зону обследования.
        :param out_point: Точка выхода из зоны обследования.
        """
        self.route_points = route_points
        self.in_point = in_point
        self.out_point = out_point

        self._create_points_genome()
        self._count_mutation_swaps()
        self._calc_route_max_distance()
        self._calc_route_max_turns_angle()
        self._calc_route_max_self_intersections()

        self._find_best_genotype()

        return self._genotype_to_route(self._best_genotype)
