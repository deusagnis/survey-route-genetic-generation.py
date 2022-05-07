"""
Реализация генетического алгоритма.
"""
import math
import logging
import numpy as np


class GeneticAlgorithm:
    def __init__(self,
                 population_size=16,
                 selection_rate=0.5,
                 parents_count=2,
                 mutants_rate=0.125,
                 max_lifecycles=128,
                 parents_choice_type="panmixia",
                 parents_similarity_type="fitness"
                 ):
        """
        :param population_size: Начальный размер популяции.
        :param selection_rate: Доля выживших при естественном отборе.
        :param parents_count: Количество родителей при размножении.
        :param mutants_rate: Доля мутантов в популяции.
        :param max_lifecycles: Максимальное количество жизненных циклов эволюции.
        :param parents_choice_type: Способ выбора родителей при размножении: panmixia, inbreeding, outbreeding.
        :param parents_similarity_type: Тип сравнения генотипов родителей при размножении: fitness, combination.
        """
        self.population_size = population_size
        self.selection_rate = selection_rate
        self.parents_count = parents_count
        self.mutants_rate = mutants_rate
        self.parents_choice_type = parents_choice_type
        self.parents_similarity_type = parents_similarity_type
        self.max_lifecycles = max_lifecycles

        self.genome = None
        self.genotype_comparison_func = None
        self.crossing_func = None
        self.mutation_func = None
        self.fitness_func = None

        self._lifecycle_counter = 0

    def _calc_mutants_count(self):
        """
        Подсчитать количества мутантов для популяции.
        """
        self._mutants_count = math.floor(self._current_population.shape[0] * self.mutants_rate)

    def _create_shuffled_genotype_indexes(self):
        """
        Создать перемешанный массив индексов генотипа.
        """
        genotype_indexes = np.arange(self._current_population.shape[0])
        np.random.shuffle(genotype_indexes)

        self._genotype_indexes = genotype_indexes

    def _calc_groups_count(self):
        """
        Подсчитать количество групп родителей в популяции.
        """
        self._parent_groups_count = math.floor(self._current_population.shape[0] / self.parents_count)

    def _choose_genotype_sort_func(self):
        """
        Выбрать функцию для сортировки генотипов при скрещивании.
        """
        if self.parents_similarity_type == "fitness":
            self._genotype_sort_func = self.fitness_func
        else:
            self._genotype_sort_func = self.genotype_comparison_func

    def _inbreeding_group_parents(self):
        """
         Группировать родителей по принципу инбридинга.
        """
        sorted_population = sorted(self._current_population, key=self._genotype_sort_func)

        parent_groups = []
        group = []
        for genotype_index in range(self._parent_groups_count * self.parents_count):
            group.append(sorted_population[genotype_index])
            if len(group) == self.parents_count:
                parent_groups.append(np.array(group))
                group = []

        self._parent_groups = np.array(parent_groups)

    def _outbreeding_group_parents(self):
        """
         Группировать родителей по принципу аутбридинга.
        """
        sorted_population = sorted(self._current_population, key=self._genotype_sort_func)

        parent_groups = []

        for group_index in range(self._parent_groups_count):
            group = []
            for group_parent_index in range(self.parents_count):
                group.append(sorted_population[group_index * self.parents_count + group_parent_index])

            parent_groups.append(group)

        self._parent_groups = np.array(parent_groups)

    def _panmixia_group_parents(self):
        """
         Группировать родителей по принципу панмиксии.
        """
        parent_groups = []
        group = []
        for genotype_index in self._genotype_indexes[:self._parent_groups_count * self.parents_count]:
            group.append(self._current_population[genotype_index])
            if len(group) == self.parents_count:
                parent_groups.append(group)
                group = []

        self._parent_groups = np.array(parent_groups)

    def _create_inbreeding_parent_groups(self):
        """
        Создать группы родителей популяции по принципу инбридинга.
        """
        self._choose_genotype_sort_func()
        self._inbreeding_group_parents()

    def _create_outbreeding_parent_groups(self):
        """
        Создать группы родителей популяции по принципу аутбридинга.
        """
        self._choose_genotype_sort_func()
        self._outbreeding_group_parents()

    def _create_panmixia_parent_groups(self):
        """
        Создать группы родителей популяции по принципу панмиксии.
        """
        self._create_shuffled_genotype_indexes()
        self._panmixia_group_parents()

    def _calc_alive_counter(self):
        self._alive_counter = math.floor(self._current_population.shape[0] * self.selection_rate)

    def _choose_best_estimations(self):
        """
        Выбрать лучшие показатели приспособленности при отборе популяции.
        """
        self._calc_alive_counter()
        population_estimation = np.flip(np.sort(self._population_estimation))

        self._best_estimations = population_estimation[:self._alive_counter]

    def _keep_alive_population(self):
        """
        Оставить в живых часть популяции после естественного отбора.
        """
        alive_population = []
        for estimation in self._best_estimations:
            genotype_index = np.where(self._population_estimation == estimation)[0][0]
            alive_population.append(self._current_population[genotype_index])
        self._current_population = np.array(alive_population)

    def _select_alive_genotypes(self):
        """
        Произвести естественный отбор в популяции.
        """
        self._choose_best_estimations()
        self._keep_alive_population()

    def _create_parents_groups(self):
        """
        Создать группы особей для размножения.
        """
        self._calc_groups_count()

        if self.parents_choice_type == "inbreeding":
            self._create_inbreeding_parent_groups()
        elif self.parents_choice_type == "outbreeding":
            self._create_outbreeding_parent_groups()
        else:
            self._create_panmixia_parent_groups()

    def _cross_population(self):
        """
        Скрестить особей групп - размножение.
        """
        children = []
        for genotypes_group in self._parent_groups:
            children.append(self.crossing_func(genotypes_group))

        if len(children) > 1:
            self._current_population = np.concatenate((self._current_population, np.array(children)))

    def _mutate_genotypes(self):
        """
        Мутировать часть генотипов.
        """
        self._create_shuffled_genotype_indexes()
        self._calc_mutants_count()
        for genotype_index in self._genotype_indexes[:self._mutants_count]:
            mutant = self.mutation_func(self._current_population[genotype_index])
            self._current_population[genotype_index] = mutant

    def _inc_lifecycle_counter(self):
        self._lifecycle_counter += 1

    def _evolve(self):
        """
        Провести один шаг эволюции.
        """
        self._select_alive_genotypes()
        self._create_parents_groups()
        self._cross_population()
        self._mutate_genotypes()
        self._estimate_population()

    def _continue_evolution(self) -> bool:
        """
        Проверить возможность продолжения эволюции.
        """
        return (self._lifecycle_counter < self.max_lifecycles
                and (not hasattr(self, "_alive_counter") or self._alive_counter > 2))

    def _choose_best_genotype(self):
        """
        Выбрать наиболее приспособленный генотип из текущей популяции.
        """
        max_estimation = np.max(self._population_estimation)
        genotype_index = np.where(self._population_estimation == max_estimation)[0][0]

        return self._current_population[genotype_index]

    def _estimate_population(self):
        """
        Оценить приспособленность особей текущей популяции.
        """
        population_estimation = []
        for genotype in self._current_population:
            population_estimation.append(self.fitness_func(genotype))

        self._population_estimation = np.array(population_estimation)

    def _evolution(self):
        """
        Эволюционировать.
        """
        while self._continue_evolution():
            logging.info("Эволюционный цикл: \t" + str(self._lifecycle_counter))
            logging.info("Размер популяции: \t" + str(self._current_population.shape[0]))
            logging.info(
                "Минимальное, среднее и максимальное значения приспособленности: " +
                "\t" + str(np.min(self._population_estimation)) +
                "\t" + str(np.average(self._population_estimation)) +
                "\t" + str(np.max(self._population_estimation))
            )
            self._evolve()
            self._inc_lifecycle_counter()

    def _gen_first_population(self):
        """
        Создать первую популяцию.
        """
        population = []
        for i in range(self.population_size):
            genotype = self.genome.copy()
            np.random.shuffle(genotype)
            population.append(genotype)

        self._current_population = np.array(population)

    def find_best_genotype(self,
                           genome,
                           fitness_func,
                           genotype_comparison_func,
                           crossing_func,
                           mutation_func
                           ):
        """
        Подобрать наилучший генотип путём эволюции.

        :param genome: Используемый геном.
        :param fitness_func: Функция приспособленности.
        :param genotype_comparison_func: Функция сравнения генотипов.
        :param crossing_func: Функция скрещивания особей.
        :param mutation_func: Функция мутации генотипа.
        """
        self.genome = genome
        self.fitness_func = fitness_func
        self.genotype_comparison_func = genotype_comparison_func
        self.crossing_func = crossing_func
        self.mutation_func = mutation_func

        self._gen_first_population()
        self._estimate_population()
        self._evolution()

        return self._choose_best_genotype()
