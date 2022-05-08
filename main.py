"""
Использование Генератора маршрута обследования на примере
"""
import time
import logging
import numpy as np

from env import ROOT_DIR
from survey_route_generation.data.vehicle_data import VehicleData
from survey_route_generation.data.mission_settings import MissionSettings
from survey_route_generation.factories.route_generator_factory import RouteGeneratorFactory
from survey_route_generation.scaffolding.geojson import save_result
from survey_route_generation.data.data_keeper import DataKeeper
from survey_route_generation.scaffolding.logging import tune_logging
from survey_route_generation.scaffolding.generator_factory import tune_generator_factory

from config import settings


def main():
    # Инициализируем директории
    log_dir = ROOT_DIR + "\\output\\logs"
    data_dir = ROOT_DIR + "\\output\\data"

    # Настраиваем логирование
    tune_logging(settings.console_log, settings.file_log, log_dir)

    # Настраиваем экспорт данных о промежуточных вычислениях
    data_keeper = DataKeeper(data_dir)

    data_keep_func = None
    if settings.export_data:
        data_keep_func = data_keeper.keep

    # Параметры БПЛА: ширина приборного зрения (м)
    vehicle_data = VehicleData(settings.vision_width)

    # Настройки полётной миссии: координаты точки начала и точки завершения миссии
    mission_settings = MissionSettings(
        settings.start_point,
        settings.end_point
    )

    # Координаты точек зоны обследования
    survey_area_points = np.array(settings.survey_area_points)

    # Создаём экземпляр фабрики генераторов маршрута
    generator_factory = RouteGeneratorFactory()

    # Настраиваем фабрику генераторов маршрута с помощью файла настроек
    tune_generator_factory(generator_factory)

    # Задаём функцию сохранения данных для экспорта
    generator_factory.data_keep_func = data_keep_func

    # Создаём экземпляр генератора маршрута
    generator = generator_factory.make()

    # Выполняем генерацию маршрута
    start_time = time.time()
    route_result = generator.generate_route(
        vehicle_data,
        mission_settings,
        survey_area_points
    )
    logging.info("Затрачено времени: \t" + str(time.time() - start_time))
    if settings.export_data:
        data_keeper.save()

    # Сохраняем найденный маршрут в формате GeoJson
    save_result(route_result, survey_area_points, mission_settings)


if __name__ == "__main__":
    main()
