"""
Агрегатор промежуточных данных.
"""
import time
import numpy as np


class DataKeeper:
    def __init__(self, save_dir):
        """
        Инициализация значений.
        :param save_dir: Директория сохранения результатов.
        """
        self.save_dir = save_dir

        self.filename = None

        self._population_size = 0
        self._event_name = None
        self._data_object = None

        self._init_data_spot()

    def _init_data_spot(self):
        """
        Инициализировать пустой спот данных.
        """
        self.data_spot = {
            "area": {},
            "route_result": {},
            "mutations": {},
            "route_fitness": {},
            "evolution": {},
            "populations": [],
            "genotypes": [],
            "estimations": [],
            "genotypes_fitness": []
        }

    def _handle_result_obtaining(self):
        """
        Обработать событие получения результата.
        """
        self.data_spot["route_result"]["in_point"] = self._data_object["in_point"]
        self.data_spot["route_result"]["route"] = self._data_object["route"]
        self.data_spot["route_result"]["route_fitness"] = self._data_object["route_fitness"]
        self.data_spot["route_result"]["route_hash"] = self._data_object["route_hash"]
        self.data_spot["route_result"]["out_point"] = self._data_object["out_point"]

    def _handle_lifecycle_step_ending(self):
        """
        Обработать событие окончания эволюционного цикла.
        """
        population = {
            "size": self._population_size,
            "elapsed_time": self._data_object.lifecycle_elapsed_time,
            "deaths": self._data_object.deaths_counter,
            "parent_groups": self._data_object.parent_groups_count,
            "children": self._data_object.children_count,
            "mutants": self._data_object.mutants_count
        }
        self.data_spot["populations"].append(population)

    def _handle_route_fitness_calculation(self):
        """
        Обработать событие вычисления функции приспособленности маршрута.
        """
        if self._data_object.route_id is None:
            return

        genotype_fitness = {
            "route_distance": self._data_object.route_distance,
            "route_turns_angle": self._data_object.route_turns_angle,
            "route_self_intersections": self._data_object.route_self_intersections,
            "normalized_route_distance": self._data_object.normalized_route_distance,
            "normalized_route_turns_angle": self._data_object.normalized_route_turns_angle,
            "normalized_route_self_intersections": self._data_object.normalized_route_self_intersections
        }
        self.data_spot["genotypes_fitness"].append(genotype_fitness)

    def _handle_lifecycle_step_beginning(self):
        """
        Обработать событие начала эволюционного цикла.
        """
        self._population_size = self._data_object.current_population.shape[0]
        self.data_spot["genotypes"].extend(self._data_object.current_population)
        self.data_spot["estimations"].extend(self._data_object.population_estimation)

    def _handle_evolution_beginning(self):
        """
        Обработать событие начала эволюции.
        """
        self.data_spot["evolution"]["population_size"] = self._data_object.population_size
        self.data_spot["evolution"]["selection_rate"] = self._data_object.selection_rate
        self.data_spot["evolution"]["parents_count"] = self._data_object.parents_count
        self.data_spot["evolution"]["mutants_rate"] = self._data_object.mutants_rate
        self.data_spot["evolution"]["parents_choice_type"] = self._data_object.parents_choice_type
        self.data_spot["evolution"]["parents_similarity_type"] = self._data_object.parents_similarity_type
        self.data_spot["evolution"]["max_lifecycles"] = self._data_object.max_lifecycles

    def _handle_genotype_search_beginning(self):
        """
        Обработать событие начала поиска лучшего генотипа.
        """
        # Static:
        self.data_spot["area"]["route_points"] = self._data_object.route_points
        self.data_spot["area"]["in_point"] = self._data_object.in_point
        self.data_spot["area"]["out_point"] = self._data_object.out_point
        self.data_spot["mutations"]["swap_rate"] = self._data_object.mutation_swap_value
        self.data_spot["route_fitness"]["distance_weight"] = self._data_object.route_distance_weight
        self.data_spot["route_fitness"]["turns_angle_weight"] = self._data_object.route_turns_angle_weight
        self.data_spot["route_fitness"]["self_intersection_weight"] = self._data_object.route_self_intersection_weight

        # Calculated:
        self.data_spot["mutations"]["swap_count"] = self._data_object.mutation_swap_count
        self.data_spot["route_fitness"]["max_distance"] = self._data_object.max_route_distance
        self.data_spot["route_fitness"]["max_turns_angle"] = self._data_object.max_route_turns_angle
        self.data_spot["route_fitness"]["max_self_intersections"] = self._data_object.max_route_self_intersections

    def _gen_filename(self):
        """
        Сгенерировать имя файла.
        """
        self.filename = self.save_dir + "\\data_" + str(time.time()) + ".npy"

    def keep(self, data_object, event_name):
        """
        Агрегировать данные.
        """
        self._data_object = data_object
        self._event_name = event_name
        if event_name == "genotype_search_beginning":
            self._handle_genotype_search_beginning()
        elif event_name == "evolution_beginning":
            self._handle_evolution_beginning()
        elif event_name == "lifecycle_step_beginning":
            self._handle_lifecycle_step_beginning()
        elif event_name == "route_fitness_calculation":
            self._handle_route_fitness_calculation()
        elif event_name == "lifecycle_step_ending":
            self._handle_lifecycle_step_ending()
        elif event_name == "result_obtaining":
            self._handle_result_obtaining()
        else:
            pass

    def save(self):
        """
        Сохранить текущий спот данных.
        """
        self._gen_filename()

        return np.save(self.filename, self.data_spot)

    def clear_spot(self):
        """
        Очистить текущий спот данных.
        """
        del self.data_spot
        self._init_data_spot()
