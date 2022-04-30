from route_generator import RouteGenerator

# init vehicle data
vehicle_data = ''
# init way settings
way_settings = ''
# init survey area points
survey_area_points = ''

route_generator = RouteGenerator(vehicle_data, way_settings, survey_area_points)

if __name__ == '__main__':
    route_generator.generate_route()
