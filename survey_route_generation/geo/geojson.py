"""
Запись и чтение географических данных из файла в формате GeoJson.
"""

import json
from os.path import exists


class GeoJson:
    """
    Начальный шаблон для формата GeoJson.
    """
    geo = {
        "type": "FeatureCollection",
        "features": []
    }

    def _add_feature(self, name, geometry_type, coordinates):
        """
        Добавить геометрический объект.
        """
        self.geo["features"].append({
            "type": "Feature",
            "properties": {
                "name": name,
            },
            "geometry": {
                "type": geometry_type,
                "coordinates": coordinates
            }
        })

    def add_point(self, name, point):
        """
        Добавить точку.
        """
        self._add_feature(name, 'Point', point)

    def add_line(self, name, points):
        """
        Добавить линию.
        """
        self._add_feature(name, 'LineString', points)

    def add_polygon(self, name, points):
        """
        Добавить полигон.
        """
        self._add_feature(name, 'Polygon', points)

    def get_feature(self, name):
        """
        Получить объект по его имени.
        """
        for feature in self.geo["features"]:
            if feature["properties"]["name"] == name:
                return feature

        return False

    def read_file(self, filename):
        """
        Считать коллекцию объектов из файла.
        """
        if not exists(filename):
            return

        f = open(filename, "r")
        content = f.read()
        f.close()

        self.geo = json.loads(content)

    def write_file(self, filename):
        """
        Записать текущую коллекцию объектов в файл.
        """

        f = open(filename, "w")
        res = f.write(json.dumps(self.geo))
        f.close()

        return res
