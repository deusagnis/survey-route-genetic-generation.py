from survey_route_generation.genetic.genetic_algorithm import GeneticAlgorithm
from survey_route_generation.genetic.genetic_optimal_route_finder import GeneticOptimalRouteFinder
from survey_route_generation.route_generator import RouteGenerator


class RouteGeneratorFactory:
    def __init__(self,
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
                 route_turns_angle_weight=None
                 ):

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
            self.route_turns_angle_weight
        )

        return RouteGenerator(
            genetic_optimal_route_finder,
        )
