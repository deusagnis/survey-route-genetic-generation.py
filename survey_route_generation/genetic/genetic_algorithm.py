import random


class GeneticAlgorithm:
    def __init__(self,
                 genome,
                 fitness_func,
                 gen_comparison_func,
                 crossing_func,
                 mutation_func,
                 population_size=16,
                 selection_rate=0.5,
                 parents_count=2,
                 mutants_rate=0.125,
                 max_lifecycles=128,
                 parents_choice_type="panmixia|inbreeding|outbreeding"
                 ):
        self.genome = genome
        self.fitness_func = fitness_func
        self.gen_comparison_func = gen_comparison_func
        self.crossing_func = crossing_func
        self.mutation_func = mutation_func
        self.population_size = population_size
        self.selection_rate = selection_rate
        self.parents_count = parents_count
        self.mutants_rate = mutants_rate
        self.parents_choice_type = parents_choice_type
        self.max_lifecycles = max_lifecycles

        self._current_population = []
        self._lifecycle_counter = 0

    def _calc_mutants_count(self):
        self._mutants_count = int(self._current_population_size * self.mutants_rate)

    def _create_shuffled_genotype_indexes(self):
        genotype_indexes = [i for i in range(self._current_population_size)]
        random.shuffle(genotype_indexes)
        self._genotype_indexes = genotype_indexes

    def _calc_groups_count(self):
        self._parent_groups_count = int(self._current_population_size / self.parents_count)

    def _create_inbreeding_parent_groups(self):
        pass

    def _create_outbreeding_parent_groups(self):
        pass

    def _create_panmixia_parent_groups(self):
        self._parent_groups = []
        self._create_shuffled_genotype_indexes()
        self._calc_groups_count()

        group = []
        for genotype_index in self._genotype_indexes[:self._parent_groups_count * self.parents_count]:
            group.append(self._current_population[genotype_index])
            if len(group) == self.parents_count:
                self._parent_groups.append(group)
                group = []

    def _choose_best_estimations(self):
        alive_count = int(self._current_population_size * self.selection_rate)
        population_estimation = sorted(self._population_estimation, reverse=True)
        self._best_estimations = population_estimation[:alive_count]

    def _keep_alive_population(self):
        alive_population = []
        for estimation in self._best_estimations:
            genotype_index = self._population_estimation.index(estimation)
            alive_population.append(self._current_population[genotype_index])
        self._current_population = alive_population

    def _select_alive_genotypes(self):
        # choose best estimations
        self._choose_best_estimations()

        # keep alive population
        self._keep_alive_population()

        # calc population size
        self._calc_current_population_size()

    def _create_parents_groups(self):
        if self.parents_choice_type == "inbreeding":
            self._create_inbreeding_parent_groups()
        elif self.parents_choice_type == "outbreeding":
            self._create_outbreeding_parent_groups()
        else:
            self._create_panmixia_parent_groups()

    def _cross_population(self):
        children = []
        for genotypes_group in self._parent_groups:
            children.append(self.crossing_func(genotypes_group))
        self._current_population.extend(children)
        self._calc_current_population_size()

    def _mutate_genotypes(self):
        self._create_shuffled_genotype_indexes()
        self._calc_mutants_count()
        for genotype_index in self._genotype_indexes[:self._mutants_count]:
            mutant = self.mutation_func(self._current_population[genotype_index])
            self._current_population[genotype_index] = mutant

    def _evolve(self):
        # selection of alive genotypes
        self._select_alive_genotypes()
        # create parent groups
        self._create_parents_groups()
        # make population crossing
        self._cross_population()
        # mutate some genotypes
        self._mutate_genotypes()
        # estimate population
        self._estimate_population()

    def _continue_evolution(self) -> bool:
        return self._lifecycle_counter < self.max_lifecycles

    def _choose_best_genotype(self):
        max_estimation = max(self._population_estimation)
        genotype_index = self._current_population.index(max_estimation)

        return self._current_population[genotype_index]

    def _estimate_population(self):
        self._population_estimation = []
        for genotype in self._current_population:
            self._population_estimation.append(self.fitness_func(genotype))

    def _evolution(self):
        while self._continue_evolution():
            self._evolve()

    def _calc_current_population_size(self):
        self._current_population_size = len(self._current_population)

    def _gen_first_population(self):
        for i in range(self.population_size):
            genotype = self.genome.copy()
            random.shuffle(genotype)
            self._current_population.append(genotype)

    def find_best_genotype(self):
        # gen first population
        self._gen_first_population()
        self._calc_current_population_size()
        self._estimate_population()
        # evolution while possible
        self._evolution()
        # choose best genotype
        return self._choose_best_genotype()
