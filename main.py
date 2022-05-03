from vehicle_data import VehicleData
from way_settings import WaySettings
from route_generator import RouteGenerator

# init vehicle data
vehicle_data = VehicleData(1, 40, 1000)

# init way settings
way_settings = WaySettings(
    [54.9611806, 20.21824722222222],
    [54.9331722, 20.370066666666666]
)

# init survey area points
survey_area_points = [
    [55.247697, 19.699547],
    [55.559281, 19.056831],
    [55.974931, 19.660008],
    [55.836542, 20.503575],
]

route_generator = RouteGenerator(vehicle_data, way_settings, survey_area_points)

if __name__ == '__main__':
    route_generator.generate_route()
