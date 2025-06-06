import requests
import pandas as pd
import geopandas as gpd

from zipfile import ZipFile
from io import BytesIO
from shapely import Point, LineString
from walk_app.helpers import proj_to_utm, convert_xy_to_point, convert_shapes_to_gdf

class gtfs:
    def __init__(self, shapes, trips, stops, routes):
        self.shapes = shapes
        self.trips = trips
        self.stops = stops
        self.routes = routes
        
    @classmethod
    def from_zip(cls, path):
        r = requests.get(path)
        z = ZipFile(BytesIO(r.content))

        routes = pd.read_csv(z.open("routes.txt"))
        trips = pd.read_csv(z.open("trips.txt"))
        
        shapes = pd.read_csv(z.open("shapes.txt"))
        shapes = convert_shapes_to_gdf(shapes)
        shapes = proj_to_utm(shapes)
        
        stops = pd.read_csv(z.open("stops.txt"))
        stops = convert_xy_to_point(stops)
        stops = proj_to_utm(stops)
        
        return cls(
            shapes=shapes,
            trips=trips,
            stops=stops,
            routes=routes
        )
    
if __name__ == "__main__":
    test_url = 'https://files.mobilitydatabase.org/mdb-1846/mdb-1846-202412230108/mdb-1846-202412230108.zip'
    wamta = gtfs.from_zip(test_url)
    print(wamta.shapes)
    print(wamta.trips)
    print(wamta.stops)
    print(wamta.routes)