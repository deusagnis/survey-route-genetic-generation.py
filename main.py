"""
Использование Генератора маршрута обследования на примере
"""
import numpy as np

from survey_route_generation.data.vehicle_data import VehicleData
from survey_route_generation.data.way_settings import MissionSettings
from survey_route_generation.route_generator import RouteGenerator

vehicle_data = VehicleData(5000)

mission_settings = MissionSettings(
    [54.9611806, 20.21824722222222],
    [54.9331722, 20.370066666666666]
)

survey_area_points = np.array([
    [55.247697, 19.699547],
    [55.559281, 19.056831],
    [55.974931, 19.660008],
    [55.836542, 20.503575],
])

route_generator = RouteGenerator(vehicle_data, mission_settings, survey_area_points)

if __name__ == '__main__':
    route = route_generator.generate_route()
    print(route)
