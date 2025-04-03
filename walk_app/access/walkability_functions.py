import numpy as np
import pandas as pd
import geopandas as gpd
# import pandanas as pdna
from warnings import warn

#TODO replace the network class

def ideal_distance(start, end, p=1.5):
    '''
    Generalized distance between points

    Parameters
    ----------
    start : gpd.GeoSeries of Points
        Point A in distance calculation; should have same number of elements
        as `end`; points will be matched in order.
    end : gpd.GeoSeries of Points
        Point B in distance calculation; should have same number of elements
        as `start`; points will be matched in order
    p : numeric, optional
        Parameter used in the distance equation; 1 is Manhattan; 2 is 
        Euclidean; values between 1 and 2 are standard for a Minkowski
        distance. The default is 1.5.

    Returns
    -------
    dist : TYPE
        DESCRIPTION.

    '''
    dist = (
        np.abs(start.geometry.x.values - end.geometry.x.values)**p +
        np.abs(start.geometry.y.values - end.geometry.y.values)**p
    ) ** (1/p)
    return dist

def access_ratio(
        self, parcel_id="id", out_dir=None, out_name=None, sum_points="centroids"
    ):
        if not self.parcels_cov.empty != False:
            warn(
                "Parcels do not fully cover summary areas "
                "interpolated values could have errors and are likely "
                "inaccurate"
            )

        if self.walk is None:
            raise ValueError("No Walk Network data provided to class")
        elif self.walk.empty:
            raise ValueError("No Walk Network intersected with Summary Areas")
        elif self.parcels is None:
            raise ValueError("No Parcels data provided to class")
        elif self.parcels.empty:
            raise ValueError("No Parcels intersected with Summary Areas")

        else:
            if isinstance(sum_points, str):
                sum_points = self.sum_areas.copy()
                sum_points.geometry = sum_points.centroid

            if isinstance(sum_points, gpd.GeoDataFrame):
                if self.sum_id not in sum_points.columns:
                    raise ValueError(f"sum_id must be present in sum_points columns")

            parcels = self.parcels_geo.copy()
            parcels.geometry = parcels.centroid
            parcels = parcels.sjoin(self.sum_areas)

            # network = Network.from_gdf(
            #     self.walk_geo, twoway="SNIFF", impedance_col="length"
            # )

            distances = []
            for stn in sum_points[self.sum_id]:
                stn_parcels = parcels.loc[parcels[self.sum_id] == stn]
                stn_loc = sum_points.loc[sum_points[self.sum_id] == stn]

                # parcel_nodes = network.pdna.get_node_ids(
                #     stn_parcels.geometry.x, stn_parcels.geometry.y
                # )
                # stn_node = network.pdna.get_node_ids(
                #     stn_loc.geometry.x, stn_loc.geometry.y
                # )

                # net_distances = network.pdna.shortest_path_lengths(
                #     pd.Series(np.repeat(stn_node, len(parcel_nodes))).to_list(), 
                #     parcel_nodes.to_list()
                #     )
                
                # par_dist = pd.DataFrame(
                #     {
                #         parcel_id: stn_parcels[parcel_id],
                #         self.sum_id: stn,
                #         "net_dist": net_distances,
                #     }
                # )

                # distances.append(par_dist)

            distances = pd.concat(distances)
            # Remove NAs
            distances = distances.loc[distances.net_dist != 4294967.295]

            ideal_distances = []
            for stn in sum_points[self.sum_id]:
                stn_parcels = parcels.loc[parcels[self.sum_id] == stn]
                stn_loc = sum_points.loc[sum_points[self.sum_id] == stn]
                ideal_dists = ideal_distance(stn_loc, stn_parcels)

                par_ideal = pd.DataFrame(
                    {
                        parcel_id: stn_parcels[parcel_id],
                        self.sum_id: stn,
                        "ideal_dist": ideal_dists,
                    }
                )

                ideal_distances.append(par_ideal)

            ideal_distances = pd.concat(ideal_distances)
            final_distances = distances.merge(ideal_distances, how="inner")

            if parcels.crs.axis_info[0].unit_name != "meter":
                final_distances["net_dist"] = final_distances["net_dist"] * 3.28084

            final_distances["ratio"] = (
                final_distances["net_dist"] / final_distances["ideal_dist"]
            )

            if out_dir != None:
                # parcels.merge(final_distances).to_file(
                #     make_path(out_dir, f"{out_name}.shp")
                # )
                pass

            final_distances.replace(0, np.NaN, inplace=True)

            final = final_distances.groupby(self.sum_id).agg(
                mean_ratio=("ratio", "mean"),
                median_ratio=("ratio", "median"),
                max_ratio=("ratio", "max"),
                min_ratio=("ratio", "min"),
                mean_net_dist=("net_dist", "mean"),
                median_net_dist=("net_dist", "median"),
                max_net_dist=("net_dist", "max"),
                min_net_dist=("net_dist", "min"),
                mean_ideal_dist=("ideal_dist", "mean"),
                median_ideal_dist=("ideal_dist", "median"),
                max_ideal_dist=("ideal_dist", "max"),
                min_ideal_dist=("ideal_dist", "min"),
            )

            return final.reset_index()