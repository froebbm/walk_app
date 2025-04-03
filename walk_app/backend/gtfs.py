import requests
import pandas as pd
from zipfile import ZipFile
from io import BytesIO

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

        shapes = pd.read_csv(z.open("shapes.txt"))
        trips = pd.read_csv(z.open("trips.txt"))
        stops = pd.read_csv(z.open("stops.txt"))
        routes = pd.read_csv(z.open("routes.txt"))
        
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