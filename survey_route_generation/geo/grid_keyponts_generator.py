"""
Создание сетки ключевых точек по заданным границам с заданными шагами по широте и долготе.
"""
import numpy as np


class GridKeypointsGenerator:
    def __init__(self, borders, lat_step, lon_step):
        self.borders = borders
        self.lon_step = lon_step
        self.lat_step = lat_step

    def _gen_grid(self):
        grid = np.array([])
        for lat in np.arange(self.borders["lat_bot"], self.borders["lat_top"] + self.lat_step, self.lat_step):
            for lon in np.arange(self.borders["lon_left"], self.borders["lon_right"] + self.lon_step, self.lon_step):
                grid = np.append(grid, [lat, lon])

        return grid

    def gen(self):
        return self._gen_grid()
