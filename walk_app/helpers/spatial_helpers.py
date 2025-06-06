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