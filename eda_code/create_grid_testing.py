import os

import pandas as pd
import geopandas as gpd

from walk_app.backend import gtfs
from walk_app.helpers import proj_to_utm
from shapely import Point
from math import ceil

half_mile = 804.672
mile = 1609.34
foot_to_meter = 0.3048
ft500 = 500*foot_to_meter

wmata = gtfs.from_zip("https://files.mobilitydatabase.org/mdb-1846/mdb-1846-202412230108/mdb-1846-202412230108.zip")
# zones = gpd.read_file("./data/World_UTM_Grid.geojson")

# utm_zone = zones.sjoin(wmata.stops.iloc[[1],:])['ZONE'].item()
# wmata.shapes = wmata.shapes.to_crs(f"EPSG:326{utm_zone}")

wmata.shapes = proj_to_utm(wmata.shapes)
wmata.stops = proj_to_utm(wmata.stops)

buffers = wmata.stops.copy()
buffers.geometry = buffers.geometry.buffer(distance = half_mile)
bounds = buffers.iloc[[1],:]['geometry'].total_bounds

# x coords
x_gap = bounds[2] - bounds[0]
x_points = ceil(gap / ft500)
x_coords = [bounds[0]+(x*ft500) for x in range(0, x_points)]

y_gap = bounds[3] - bounds[1]
y_points = ceil(gap / ft500)
y_coords = [bounds[1]+(x*ft500) for x in range(0, y_points)]

points = []
for x in x_coords:
    for y in y_coords:
        points.append(Point(x,y))

grid = gpd.GeoDataFrame(index = [x for x in range(0, len(points))],
                        geometry = points,
                        crs=wmata.stops.crs)

grid.explore()
