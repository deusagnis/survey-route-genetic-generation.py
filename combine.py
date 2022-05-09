"""
Комбинирование разных параметров генерации маршрута в целях поиска оптимальных и исследования их зависимостей.
"""
import numpy as np

from config import settings

from survey_route_generation.data.data_keeper import DataKeeper
from survey_route_generation.data.mission_settings import MissionSettings
from survey_route_generation.data.vehicle_data import VehicleData
from survey_route_generation.factories.route_generator_factory import RouteGeneratorFactory
from survey_route_generation.combinator.combinator import Combinator
from survey_route_generation.scaffolding.dirs import DATA_DIR


def main():
    data_keeper = DataKeeper(DATA_DIR)

    generator_factory = RouteGeneratorFactory()

    generator_factory.max_lifecycles = 512
    generator_factory.mutation_swap_type = "rate"
    generator_factory.data_keep_func = data_keeper.keep

    # Диапазоны параметров для комбинации
    params_ranges = settings.params_ranges

    # Параметры БПЛА: ширина приборного зрения (м)
    vehicle_data = VehicleData(settings.vision_width)
    # Настройки полётной миссии: координаты точки начала и точки завершения миссии
    mission_settings = MissionSettings(
        settings.start_point,
        settings.end_point
    )
    # Координаты точек зоны обследования
    survey_area_points = np.array(settings.survey_area_points)

    # Создаём экземпляр комбинатора параметров
    combinator = Combinator(
        generator_factory,
        params_ranges,
        vehicle_data,
        mission_settings,
        survey_area_points,
        data_keeper,
        11
    )

    # Комбинируем параметры относительно поиска оптимальных маршрутов
    combinator.combine()

    # Сохраняем топ результатов
    combinator.save()


if __name__ == "__main__":
    main()
