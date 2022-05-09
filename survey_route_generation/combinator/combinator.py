"""
Перебор всех комбинаций заданных параметров с сохранением нескольких наилучших.
"""
import sys
import time
import signal

from survey_route_generation.console.console import cls
from survey_route_generation.scaffolding.geojson import save_result


class Combinator:
    def __init__(
            self,
            factory,
            params_ranges,
            vehicle_data,
            mission_settings,
            survey_area_points,
            data_keeper,
            top_size=11
    ):
        """
        Инициализировать параметры для перебора.
        :param factory: Фабрика генераторов маршрута.
        :param params_ranges: Диапазоны перебираемых параметров.
        :param vehicle_data: Данные БПЛА.
        :param mission_settings: Данные полётной миссии.
        :param survey_area_points: Данные зоны обследования.
        :param data_keeper: Хранитель данных.
        :param top_size: Размер выборки наилучших слепков данных.
        """
        self.factory = factory
        self.params_ranges = params_ranges
        self.vehicle_data = vehicle_data
        self.mission_settings = mission_settings
        self.survey_area_points = survey_area_points
        self.data_keeper = data_keeper
        self.top_size = top_size

        self.combination_counter = 0
        self.time_behind = 0
        self.top_data_spots = []

        self._calc_combinations_amount()
        self._subscribe_signals()

    def _subscribe_signals(self):
        signal.signal(signal.SIGINT, self._early_exit)
        signal.signal(signal.SIGTERM, self._early_exit)

    def _early_exit(self, _signum, _frame):
        print("Сохраняем результат...")
        self.save()
        sys.exit(0)

    def _insert_data_spot(self):
        """
        Вставить спот данных в отсортированный список.
        """
        insert_index = None
        for data_spot_index in range(len(self.top_data_spots) - 2, -1, -1):
            if (
                    self.top_data_spots[data_spot_index]["route_result"]["route_fitness"]
                    < self.data_keeper.data_spot["route_result"]["route_fitness"]
            ):
                insert_index = data_spot_index
                if data_spot_index > 0:
                    self.top_data_spots[data_spot_index] = self.top_data_spots[data_spot_index - 1]
            else:
                break
        if insert_index is not None:
            self.top_data_spots[insert_index] = self.data_keeper.data_spot.copy()

    def _append_data_spot(self):
        """
        Добавить спот данных в список лучших и поддержать
        """
        self.top_data_spots.append(self.data_keeper.data_spot.copy())
        self.top_data_spots.sort(key=lambda data_spot: data_spot["route_result"]["route_fitness"], reverse=True)

    def _current_spots_have_route(self, route_hash):
        """
        Проверить, есть ли текущий спот данных в списке сохранённых.
        """
        for data_spot in self.top_data_spots:
            if data_spot["route_result"]["route_hash"] == route_hash:
                return True

        return False

    def _calc_combinations_amount(self):
        """
        Подсчитать количество комбинаций.
        """
        self.combinations_amount = 1

        for param_range in self.params_ranges.values():
            self.combinations_amount *= len(param_range)

    def _calc_elapsed_time(self):
        """
        Посчитать затраченное время последней обработки комбинации.
        """
        self.elapsed_time = time.time() - self.combination_start_time

    def _calc_time_behind(self):
        """
        Посчитать время работы.
        """
        self.time_behind += self.elapsed_time

    def _analyze_result(self):
        """
        Выполнить анализ результата применения параметров комбинации.
        """
        self._calc_elapsed_time()

        if self._current_spots_have_route(self.data_keeper.data_spot["route_result"]["route_hash"]):
            return

        if len(self.top_data_spots) < self.top_size:
            self._append_data_spot()
        else:
            self._insert_data_spot()

    def _inc_combination_counter(self):
        """
        Инкриминировать счётчик комбинаций.
        """
        self.combination_counter += 1

    def _show_progress(self):
        """
        Вывести прогресс в консоль.
        """
        percent = (self.combination_counter / self.combinations_amount) * 100
        combination = [
            self.factory.population_size,
            self.factory.selection_rate,
            self.factory.parents_count,
            self.factory.mutants_rate,
            self.factory.parents_choice_type,
            self.factory.parents_similarity_type,
            self.factory.mutation_swap_value,
            self.factory.route_distance_weight,
            self.factory.route_turns_angle_weight,
            self.factory.route_self_intersection_weight,
            self.factory.repair_route_genotypes
        ]

        cls()
        print("Прошло времени: ", self.time_behind, "секунд")
        print(percent, "%", "[", self.combination_counter, "/", self.combinations_amount, "]")
        print(combination)

    def _handle_combination(self):
        """
        Обработать текущую комбинацию - применить параметры.
        """
        self._inc_combination_counter()

        self.generator = self.factory.make()

        self.combination_start_time = time.time()
        self.route_result = self.generator.generate_route(
            self.vehicle_data,
            self.mission_settings,
            self.survey_area_points
        )
        self.data_keeper.keep(self.route_result, "result_obtaining")

        self._analyze_result()
        self.data_keeper.clear_spot()
        self._calc_time_behind()

    def combine(self):
        """
        Выполнить комбинацию параметров.
        """
        for population_size in self.params_ranges["population_size"]:
            self.factory.population_size = population_size
            for selection_rate in self.params_ranges["selection_rate"]:
                self.factory.selection_rate = selection_rate
                for parents_count in self.params_ranges["parents_count"]:
                    self.factory.parents_count = parents_count
                    for mutants_rate in self.params_ranges["mutants_rate"]:
                        self.factory.mutants_rate = mutants_rate
                        for parents_choice_type in self.params_ranges["parents_choice_type"]:
                            self.factory.parents_choice_type = parents_choice_type
                            for parents_similarity_type in self.params_ranges["parents_similarity_type"]:
                                self.factory.parents_similarity_type = parents_similarity_type
                                for mutation_swap_value in self.params_ranges["mutation_swap_value"]:
                                    self.factory.mutation_swap_value = mutation_swap_value
                                    for route_distance_weight in self.params_ranges["route_distance_weight"]:
                                        self.factory.route_distance_weight = route_distance_weight
                                        for route_turns_angle_weight in self.params_ranges["route_turns_angle_weight"]:
                                            self.factory.route_turns_angle_weight = route_turns_angle_weight
                                            for route_self_intersection_weight in self.params_ranges[
                                                "route_self_intersection_weight"]:
                                                self.factory.route_self_intersection_weight = route_self_intersection_weight
                                                for repair_route_genotypes in self.params_ranges[
                                                    "repair_route_genotypes"]:
                                                    self.factory.repair_route_genotypes = repair_route_genotypes

                                                    self._handle_combination()
                                                    self._show_progress()

    def save(self):
        """
        Сохранить лучшие выбранные споты данных.
        """
        for data_spot in self.top_data_spots:
            self.data_keeper.data_spot = data_spot
            self.data_keeper.save()

            save_result(data_spot["route_result"], self.survey_area_points, self.mission_settings)
