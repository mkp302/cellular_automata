from models.cell import Cell
import random
from PIL import Image
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_bounds
import numpy as np
from pyproj import Transformer
import math


def angle_between_vectors(v1, v2):
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_theta = np.clip(cos_theta, -1, 1)
    return np.arccos(cos_theta)


class Grid:
    def __init__(self, N, max_N, min_N):
        self.N = N
        self.max_N = max_N
        self.min_N = min_N
        self.cells = []
        im = Image.open("stencil_3.png")
        pixels = list(im.getdata())
        i = 0
        # Rows/Cols so 0,0 is top left

        for _ in range(0, N + 2):
            row = []
            for _ in range(0, N + 2):
                cell = Cell.generate_cell()
                if pixels[i][3] >= 100:
                    cell.burning = 1
                else:
                    cell.burning = 0
                row.append(cell)
                i += 1
            self.cells.append(row)
        self.cells[210][200].burning = 2
        # Set elevation
        with rasterio.open("data/elevation.tif") as src:
            data = src.read(1)  # read the first band
            height, width = data.shape  # should be 300, 300
            print(height, width)
            rows = len(self.cells)  # 302
            cols = len(self.cells[0])  # 302

            lat_top = 47.97
            lon_left = -53.284
            lat_bottom = 47.78
            lon_right = -53.017

            dst_width = 302
            dst_height = 302
            dst_crs = "EPSG:3857"
            tf = Transformer.from_crs("EPSG:4326", dst_crs, always_xy=True)
            minx, miny = tf.transform(lon_left, lat_bottom)  # west, south
            maxx, maxy = tf.transform(lon_right, lat_top)  # east, north

            left, right = min(minx, maxx), max(minx, maxx)
            bottom, top = min(miny, maxy), max(miny, maxy)
            dst_transform = from_bounds(left, bottom, right, top, dst_width, dst_height)

            dst_array = np.full((dst_height, dst_width), np.nan, dtype=np.float32)
            reproject(
                source=rasterio.band(src, 1),
                destination=dst_array,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=dst_transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear,
            )

            for i in range(0, rows):
                for j in range(0, cols):
                    elev = float(dst_array[i, j])
                    self.cells[i][j].elevation = elev

    def set_N(self, new_N):
        if new_N > self.max_N:
            new_N = self.max_N
        if new_N < self.min_N:
            new_N = self.min_N

        if new_N > self.N:
            for row in self.cells:
                for _ in range(0, new_N - self.N):
                    cell = Cell.generate_cell()
                    row.append(cell)
        elif self.N < new_N:
            for row in self.cells:
                row = row[: new_N + 2]
        self.N = new_N
        return new_N

    def update_cells(self, wind=(0.6, 0.8), temp=20, humidity=0.4):
        intial_spread_rate = 0.3  # m/min
        fuel_configuratin_ks = 1.2

        new_grid = [[Cell() for _ in range(self.N + 2)] for _ in range(self.N + 2)]
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                new_grid[i][j].elevation = cell.elevation
                new_grid[i][j].burning = cell.burning
                new_grid[i][j].burn_count = cell.burn_count
                new_grid[i][j].spread = cell.spread

        directions = [
            (1, 0),  # s
            (1, -1),  # sw
            (0, -1),  # w
            (-1, -1),  # nw
            (-1, 0),  # n
            (-1, 1),  # ne
            (0, 1),  # e
            (1, 1),  # se
        ]
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if i == 0 or j == 0 or i == self.N + 1 or j == self.N + 1:
                    continue
                if cell.burning == 3 or cell.burning == 1:
                    continue

                if cell.burning == 2:
                    new_grid[i][j].burn_count += 1
                    if new_grid[i][j].burn_count > 10:
                        new_grid[i][j].burning = 3
                    for dy, dx in directions:
                        ni, nj = i + dx, j + dy
                        neighbour = self.cells[ni][nj]

                        if neighbour.burning != 1:
                            continue

                        # positive is downhill
                        delta_elevation = (
                            self.cells[i][j].elevation - neighbour.elevation
                        )

                        wind_x, wind_y = wind
                        wind_vec = np.array([wind_x, wind_y])

                        cell_x = 90 * dx
                        cell_y = -1 * 90 * dy
                        spread_vec = np.array([cell_x, cell_y])

                        cell_dist = math.hypot(cell_x, cell_y)
                        V = math.hypot(wind_x, wind_y)
                        theta = angle_between_vectors(spread_vec, wind_vec)
                        R = 0
                        if delta_elevation > 0:
                            slope = np.arctan(delta_elevation / cell_dist)

                            R = (
                                0.969
                                * intial_spread_rate
                                * fuel_configuratin_ks
                                * np.exp(
                                    -3.533 * abs(np.tan(slope * np.cos(theta))) ** 1.2
                                )
                                * np.exp(0.182 * V)
                            )
                        elif delta_elevation < 0:
                            slope = np.arctan(delta_elevation / cell_dist)
                            R = (
                                0.969
                                * intial_spread_rate
                                * fuel_configuratin_ks
                                * np.exp(
                                    3.533 * abs(np.tan(slope) * np.cos(theta)) ** 1.2
                                )
                                * np.exp(0.182 * V)
                            )

                        else:
                            R = (
                                0.969
                                * intial_spread_rate
                                * fuel_configuratin_ks
                                * np.exp(0.182 * V * np.cos(theta))
                            )
                        key = (dx, dy)

                        spread_dist = new_grid[i][j].spread.get(key, 0) + R * 30

                        new_grid[i][j].spread[key] = spread_dist

                        if spread_dist > cell_dist:
                            new_grid[ni][nj].burning = 2
        self.cells = new_grid

    def randomize(self):
        for i, row in enumerate(self.cells[1 : self.N + 1]):
            for j, cell in enumerate(row[1 : self.N + 1]):
                cell.tree_density = random.random()
                cell.burning = 0
                cell.burn_count = 0
        i = random.randint(1, self.N)
        j = random.randint(1, self.N)
        self.cells[i][j].burning = 2

    def reset(self):
        self.cells = []
        im = Image.open("stencil.png")
        pixels = list(im.getdata())
        i = 0
        for _ in range(0, self.N + 2):
            row = []
            for _ in range(0, self.N + 2):
                cell = Cell.generate_cell()
                if pixels[i][0] >= 10:
                    cell.burning = 0
                else:
                    cell.burning = 1
                row.append(cell)
                i += 1
            self.cells.append(row)
        self.cells[90][55].burning = 2

    def randomize_topology(self): ...
    def print_cells(self):

        for i, row in enumerate(self.cells[1 : self.N + 1]):
            for j, cell in enumerate(row[1 : self.N + 1]):
                print(cell.burning, sep=" ", end=" ")
            print("\n")
