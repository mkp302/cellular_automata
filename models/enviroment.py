import xarray as xr
import numpy as np
import math


class Enviroment:
    def __init__(self):
        self.wind_speed = (0, 0)
        self.wind_angle = 0
        self.humidity = 0
        self.dew_point = 0
        self.temperature = 0

    def update(self, time_stamp):

        ds = xr.open_dataset("data/test_2.grib", engine="cfgrib")
        data = ds.sel({"time": time_stamp}, method="nearest")
        u = float(data["u10"].values)
        v = float(data["v10"].values)
        temperature = float(data["t2m"].values) - 273.15
        dew = float(data["d2m"].values) - 273.15

        self.wind_speed = (u, v)
        self.wind_angle = math.atan2(u, v)
        self.temperature = temperature
        self.dew_point = dew
