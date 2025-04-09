import os
import geopandas as gpd

dir = os.path.dirname(__file__)


UTM_GRID = gpd.read_file(os.path.join(dir, "World_UTM_Grid.geojson"))