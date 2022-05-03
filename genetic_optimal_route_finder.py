import random
from geo import calc_distance, calc_3_points_angle
from genetic_algorithm import GeneticAlgorithm


class GeneticOptimalRouteFinder:
    def __init__(self,
                 route_points,
                 in_point,
                 out_point,
                 mutation_swap_value=0.2,
                 mutation_swap_type="percent",
                 route_distance_weight=2,
                 route_turns_angle_weight=1.5
                 ):
        self.route_points = route_points
        self.in_point = in_point
        self.out_point = out_point
        self.mutation_swap_value = mutation_swap_value
        self.mutation_swap_type = mutation_swap_type
        self.route_distance_weight = route_distance_weight
        self.route_turns_angle_weight = route_turns_angle_weight

    def _calc_route_fitness(self):
        return (self._normalized_route_turns_angle * self.route_turns_angle_weight -
                self._normalized_route_distance * self.route_distance_weight +
                self.route_distance_weight + self.route_turns_angle_weight
                )

    def _normalize_route_turns_angle(self):
        self._normalized_route_turns_angle = self._route_turns_angle / self._max_route_turns_angle

    def _normalize_route_distance(self):
        self._normalized_route_distance = self._route_distance / self._max_route_distance

    def _add_route_angles(self, route):
        for i in range(len(route) - 2):
            point = self._get_gen_point(route[i])
            next_point = self._get_gen_point(route[i + 1])
            after_next_point = self._get_gen_point(route[i + 2])

            self._route_turns_angle = calc_3_points_angle(point, next_point, after_next_point)

    def _add_start_end_angles(self, route):
        first_point = self._get_gen_point(route[0])
        second_point = self._get_gen_point(route[1])
        last_point = self._get_gen_point(len(route) - 1)
        pre_last_point = self._get_gen_point(len(route) - 2)

        self._route_turns_angle += calc_3_points_angle(self.in_point, first_point, second_point)
        self._route_turns_angle += calc_3_points_angle(pre_last_point, last_point, self.out_point)

    def _add_route_distance(self, route):
        for i in range(len(route) - 1):
            point = self._get_gen_point(route[i])
            next_point = self._get_gen_point(route[i + 1])

            self._route_distance += calc_distance(point, next_point)

    def _add_start_end_distances(self, route):
        first_point = self._get_gen_point(route[0])
        last_point = self._get_gen_point(len(route) - 1)

        self._route_distance += calc_distance(self.in_point, first_point)
        self.route_points += calc_distance(last_point, self.out_point)

    def _calc_route_turns_angle(self, route):
        self._route_turns_angle = 0
        # add start/end angles
        self._add_start_end_angles(route)
        # add route angles
        self._add_route_angles(route)

    def _calc_route_distance(self, route):
        self._route_distance = 0
        # add route distance with start/end
        self._add_start_end_distances(route)
        # add just route distance
        self._add_route_distance(route)

    def _route_fitness(self, route):
        # calc route distance
        self._calc_route_distance(route)
        # calc turns angle
        self._calc_route_turns_angle(route)
        # normalize values
        self._normalize_route_distance()
        self._normalize_route_turns_angle()
        # return estimation value

    def _cross_routes(self, route_group):
        points_usage = [False for _i in range(self._genotype_size)]

        child_genotype = []

        for i in range(self._genotype_size):
            for genotype in route_group:
                point_index = genotype[i]
                if not points_usage[point_index]:
                    child_genotype.append(point_index)
                    points_usage[point_index] = True

        return child_genotype

    def _mutate_route(self, route):
        for i in range(self._mutation_swap_count):
            index1 = random.randint(0, self._genotype_size - 1)
            index2 = random.randint(0, self._genotype_size - 1)
            temp = route[index1]
            route[index1] = route[index2]
            route[index2] = temp

        return route

    def _calc_max_turns_angle(self):
        self._max_route_turns_angle = 3.14 * self._genotype_size

    def _calc_route_max_distance(self):
        self._max_route_distance = calc_distance(
            self.route_points[0],
            self.route_points[self._genotype_size - 1]
        ) * self._genotype_size * 10

    def _count_mutation_swaps(self):
        if self.mutation_swap_type == "percent":
            self._mutation_swap_count = int(self._genotype_size * self.mutation_swap_value)
        else:
            self._mutation_swap_count = self.mutation_swap_value

    def _calc_genotype_size(self):
        self._genotype_size = len(self.route_points)

    def _get_gen_point(self, gen):
        return self.route_points[gen]

    def _create_points_genome(self):
        self._points_genome = [i for i in range(len(self.route_points))]

    def find(self):
        # create genome
        self._create_points_genome()
        # calc genotype size
        self._calc_genotype_size()
        # calc mutation swaps
        self._count_mutation_swaps()
        # calc max distance
        self._calc_route_max_distance()
        # calc max turns angle
        self._calc_max_turns_angle()

        genetic_algo = GeneticAlgorithm(
            self._points_genome,
            self._route_fitness,
            lambda a: a,
            self._cross_routes,
            self._mutate_route
        )

        return genetic_algo.find_best_genotype()