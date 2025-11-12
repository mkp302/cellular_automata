import xarray as xr
import numpy as np
from datetime import datetime, timedelta, timezone


def get_time_coord_name(ds):
    # prefer 'valid_time' if present, else 'time'
    if "valid_time" in ds.coords:
        return "valid_time"
    if "time" in ds.coords:
        return "time"
    raise RuntimeError("No time-like coordinate found in dataset.")


def select_nearest(ds, target_dt):
    coord = get_time_coord_name(ds)
    print(coord)
    return ds.sel({"time": target_dt}, method="nearest")

    # xarray supports sel(..., method="nearest") if coords are datetimes
    try:
        return ds.sel({coord: target_dt}, method="nearest")
    except Exception:
        print("Fallback")
        # fallback: compute index manually
        times = ds[coord].values
        # ensure numpy datetimes
        diffs = np.abs(times - np.datetime64(target_dt))
        idx = int(diffs.argmin())
        return ds.isel({coord: idx})


# --- Load your GRIB file (replace with your path) ---
# Example: "era5_sample.grib"
ds = xr.open_dataset("data/test_2.grib", engine="cfgrib")

sim_time = datetime(2025, 8, 3, 0, 0)
dt_minutes = 30
print(ds)


for step in range(48 * 3):  # example loop
    # choose nearest or interpolate
    nearest = select_nearest(ds, sim_time)
    u = float(nearest["u10"].values)
    v = float(nearest["v10"].values)
    tempeture = float(nearest["t2m"].values) - 273.15
    dew = float(nearest["d2m"].values) - 273.15

    # or do interpolation:
    # interp = ds.interp({get_time_coord_name(ds): np.datetime64(sim_time)})
    # u = float(interp["u10"].values); v = float(interp["v10"].values)

    print(sim_time.isoformat(), "u,v=", u, v, "temp=", tempeture, "dew point=", dew)

    # run simulation update here...

    sim_time += timedelta(minutes=dt_minutes)
