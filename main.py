"""
Использование Генератора маршрута обследования на примере
"""
import time
import numpy as np
from survey_route_generation.data.vehicle_data import VehicleData
from survey_route_generation.data.mission_settings import MissionSettings
from survey_route_generation.factories.route_generator_factory import RouteGeneratorFactory
from survey_route_generation.geo.geojson import GeoJson
from os.path import dirname, abspath

ROOT_DIR = dirname(abspath(__file__))

# Параметры БПЛА: ширина приборного зрения (м)
vehicle_data = VehicleData(13000)

# Настройки полётной миссии: координаты точки начала и точки завершения миссии
mission_settings = MissionSettings(
    [54.9611806, 20.21824722222222],
    [54.9331722, 20.370066666666666]
)

# Координаты точек зоны обследования
survey_area_points = np.array([
    [55.247697, 19.699547],
    [55.559281, 19.056831],
    [55.974931, 19.660008],
    [55.836542, 20.503575],
])

generator_factory = RouteGeneratorFactory()

# Размер начальной популяции
generator_factory.population_size = 256
# Доля выживших особей при отборе
generator_factory.selection_rate = 0.667
# Количество генотипов при размножении
generator_factory.parents_count = 2
# Доля мутированных особей
generator_factory.mutants_rate = 0.05
# Максимальное число циклов смены популяции
generator_factory.max_lifecycles = 128
# Тип выбора родительских генотипов при скрещивании: panmixia, inbreeding, outbreeding
generator_factory.parents_choice_type = "panmixia"
# Тип сравнения генотипов при группировке родителей методами аутбридинга и инбридинга: fitness, combination
generator_factory.parents_similarity_type = "fitness"
# Число мутаций в генотипе
generator_factory.mutation_swap_value = 0.1
# Тип числа мутаций: доля или конкретное число
generator_factory.mutation_swap_type = "percent"
# Значимость сокращения длины маршрута при оценке приспособленности
generator_factory.route_distance_weight = 1.5
# Значимость увеличения плавности движения при оценке приспособленности
generator_factory.route_turns_angle_weight = 1
# Значимость количества самопересений маршрута при оценке приспособленности
generator_factory.route_self_intersection_weight = 1.5

generator = generator_factory.make()

route = generator.generate_route(
    vehicle_data,
    mission_settings,
    survey_area_points
)


geojson = GeoJson()

filename = "results\\" + str(time.time()) + "_route.json"

polygon_coords = [survey_area_points[:, [1, 0]].tolist()]
polygon_coords[0].append(polygon_coords[0][0])

start_coord = mission_settings.start_point[::-1]
end_coord = mission_settings.end_point[::-1]

in_coord = route["in_point"][::-1].tolist()
out_coord = route["out_point"][::-1].tolist()

route_coords = route["route"][:, [1, 0]].tolist()

route_coords.insert(0, in_coord)
route_coords.insert(0, start_coord)
route_coords.append(out_coord)
route_coords.append(end_coord)

geojson.add_polygon("SurveyArea", polygon_coords)
geojson.add_point("Start", start_coord)
geojson.add_point("End", end_coord)
geojson.add_point("InPoint", in_coord)
geojson.add_line("Route", route_coords)
geojson.add_point("OutPoint", out_coord)

geojson.write_file(filename)
