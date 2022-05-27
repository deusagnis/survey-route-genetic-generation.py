from ipyleaflet import Polygon, Marker, AntPath, Map
from ipywidgets import HTML


def show_route_result(
        start_point,
        area_points,
        end_point,
        route_result
):
    """
    Показать результат сгенерированного маршрута в JupyterNotebook.
    """
    area_polygon = Polygon(
        locations=area_points,
        stroke_color='blue',
        fill_color='blue'
    )

    start_end_points = [
        start_point,
        end_point
    ]
    start_end_points_info = [
        {"name": "Start"},
        {"name": "End"}
    ]
    info_box_template = """
    <dl>
    <dt>Name</dt><dd>{name}</dd>
    </dl>
    """
    start_end_points_text = [info_box_template.format(**point_info) for point_info in start_end_points_info]

    start_end_markers = [Marker(location=(start_end_points[i])) for i in range(len(start_end_points))]

    ant_path = AntPath(
        locations=[
            start_point,
            route_result["in_point"],
            *route_result["route"],
            route_result["out_point"],
            end_point
        ],
        dash_array=[1, 10],
        delay=1000,
        color='#7590ba',
        pulse_color='#3f6fba'
    )

    route_m = Map(center=start_point, zoom=9)

    for i in range(len(start_end_markers)):
        start_end_markers[i].popup = HTML(start_end_points_text[i])
        route_m.add_layer(start_end_markers[i])
    route_m.add_layer(area_polygon)
    route_m.add_layer(ant_path)

    return route_m
