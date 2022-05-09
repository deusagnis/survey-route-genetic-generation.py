import time

from survey_route_generation.geo.geojson import GeoJson
from survey_route_generation.scaffolding.dirs import RESULTS_DIR


def save_result(route_result, survey_area_points, mission_settings):
    geojson = GeoJson()

    result_file = RESULTS_DIR + "\\route_" + str(time.time()) + ".json"

    polygon_coords = [survey_area_points[:, [1, 0]].tolist()]
    polygon_coords[0].append(polygon_coords[0][0])

    start_coord = mission_settings.start_point[::-1]
    end_coord = mission_settings.end_point[::-1]

    in_coord = route_result["in_point"][::-1].tolist()
    out_coord = route_result["out_point"][::-1].tolist()

    route_coords = route_result["route"][:, [1, 0]].tolist()

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

    return geojson.write_file(result_file)
