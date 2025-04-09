import os

import pandas as pd
import geopandas as gpd

from walk_app.backend import gtfs
from walk_app.helpers import proj_to_utm

os.getcwd()

wmata = gtfs.from_zip("https://files.mobilitydatabase.org/mdb-1846/mdb-1846-202412230108/mdb-1846-202412230108.zip")
# zones = gpd.read_file("./data/World_UTM_Grid.geojson")

# utm_zone = zones.sjoin(wmata.stops.iloc[[1],:])['ZONE'].item()
# wmata.shapes = wmata.shapes.to_crs(f"EPSG:326{utm_zone}")

wmata.shapes = proj_to_utm(wmata.shapes)

print(wmata.shapes.crs.is_projected)