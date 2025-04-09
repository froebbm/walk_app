import pandas as pd
import geopandas as gpd

from walk_app.data import UTM_GRID as zones

#TODO raise proper errors

n_hemi = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
s_hemi = ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def find_utm_code(gdf):
    utm_zone = zones.sjoin(gdf.iloc[[1],:])['ZONE'].item()
    utm_row = zones.sjoin(gdf.iloc[[1],:])['ZONE'].item()
    return utm_zone, utm_row

def proj_to_utm(gdf):
    
    utm_zone, utm_row = find_utm_code(gdf)
    if utm_row in n_hemi:
        gdf = gdf.to_crs(f"EPSG:326{utm_zone}")
    else:
        gdf = gdf.to_crs(f"EPSG:327{utm_zone}")
        
    return gdf
    
    