import json
from os.path import exists


class GeoJson:
    geo = {
        "type": "FeatureCollection",
        "features": []
    }

    def _add_feature(self, name, geometry_type, coordinates):
        self.geo["features"].append({
            "type": "feature",
            "properties": {
                "name": name,
            },
            "geometry": {
                "type": geometry_type,
                "coordinates": coordinates
            }
        })

    def add_point(self, name, point):
        self._add_feature(name, 'Point', point)

    def add_line(self, name, points):
        self._add_feature(name, 'LineString', points)

    def add_polygon(self, name, points):
        self._add_feature(name, 'Polygon', points)

    def get_feature(self, name):
        for feature in self.geo["features"]:
            if feature["properties"]["name"] == name:
                return feature

        return False

    def read_file(self, filename):
        if not exists(filename):
            return

        f = open(filename, "r")
        content = f.read()
        f.close()

        self.geo = json.loads(content)

    def write_file(self, filename):
        if not exists(filename):
            return False

        f = open(filename, "w")
        res = f.write(json.dumps(self.geo))
        f.close()

        return res
