import requests
import pandas as pd
import geopandas as gpd

from zipfile import ZipFile
from io import BytesIO
from shapely import Point, LineString

def convert_xy_to_point(df, lat="stop_lat", lon="stop_lon"):
    pt_geo = [Point(xy) for xy in zip(df[lon],df[lat])]
    pts = gpd.GeoDataFrame(df, geometry=pt_geo, crs="wgs84")
    return pts

def convert_shapes_to_gdf(df, lon='shape_pt_lon', lat='shape_pt_lat'):
    pts = convert_xy_to_point(df, lon=lon, lat=lat)
    
    lines = pts.groupby('shape_id')['geometry'].apply(
        lambda x: LineString(x.tolist())
        )
    
    lines = gpd.GeoDataFrame(lines, geometry="geometry", crs="wgs84")
    return lines

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
        
        stops = pd.read_csv(z.open("stops.txt"))
        stops = convert_xy_to_point(stops)
        
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