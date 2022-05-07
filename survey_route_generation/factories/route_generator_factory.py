from survey_route_generation.genetic.genetic_algorithm import GeneticAlgorithm
from survey_route_generation.genetic.genetic_optimal_route_finder import GeneticOptimalRouteFinder
from survey_route_generation.route_generator import RouteGenerator
import logging
import time


class RouteGeneratorFactory:
    def __init__(self,
                 log_dir,
                 population_size=None,
                 selection_rate=None,
                 parents_count=None,
                 mutants_rate=None,
                 max_lifecycles=None,
                 parents_choice_type=None,
                 parents_similarity_type=None,
                 mutation_swap_value=None,
                 mutation_swap_type=None,
                 route_distance_weight=None,
                 route_turns_angle_weight=None,
                 route_self_intersection_weight=None
                 ):

        self.log_dir = log_dir
        self.population_size = population_size,
        self.selection_rate = selection_rate,
        self.parents_count = parents_count,
        self.mutants_rate = mutants_rate,
        self.max_lifecycles = max_lifecycles,
        self.parents_choice_type = parents_choice_type
        self.parents_similarity_type = parents_similarity_type

        self.mutation_swap_value = mutation_swap_value
        self.mutation_swap_type = mutation_swap_type
        self.route_distance_weight = route_distance_weight
        self.route_turns_angle_weight = route_turns_angle_weight
        self.route_self_intersection_weight = route_self_intersection_weight

        self._tune_logging()

    def _tune_logging(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        file_handler = logging.FileHandler(self._gen_filename(), mode="w", encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                console_handler,
                file_handler
            ]
        )

    def _gen_filename(self):
        return self.log_dir + "\\log_" + str(time.time()) + ".log"

    def make(self):
        genetic_algo = GeneticAlgorithm(
            self.population_size,
            self.selection_rate,
            self.parents_count,
            self.mutants_rate,
            self.max_lifecycles,
            self.parents_choice_type,
            self.parents_similarity_type
        )

        genetic_optimal_route_finder = GeneticOptimalRouteFinder(
            genetic_algo,
            self.mutation_swap_value,
            self.mutation_swap_type,
            self.route_distance_weight,
            self.route_turns_angle_weight,
            self.route_self_intersection_weight
        )

        return RouteGenerator(
            genetic_optimal_route_finder,
        )
