from scipy.spatial import ConvexHull
import pandas
import numpy as np
import geojson
import time


partitions_min = np.array([10,15,20,30,40,50,60,70,80,90,120,150,180,210,240])
partitions_sec = partitions_min*60
palette = ["#478dbb","#bb631b","#d7cf4d","#c71456","#b28e8e","#f2a0b5","#7d194e","#2b9db4","#412a30","#c19fa8","#8b184f","#6e4504","#c6c6d4","#3a6c90","#6B1A6A","#769600","#FF8900","#DB2218","#8C091E","#FF931C","#E82759","#630034","#EACFB8","#457DBB","#4D664A","#6B1A6A","#769600","#A9FFF4"]

def seconds_to_hours(sec):
    ty_res = time.gmtime(sec)
    res = time.strftime("%H:%M:%S",ty_res)
    return res


def create_isochrones_hulls(graph,start,time,PandaV,partitions_sec=partitions_sec,palette=palette):
    arrayT = graph.isochrones(start,time,partitions_sec)
    XY = PandaV[["stop_lat","stop_lon"]]
    T = pandas.Series(arrayT,name="time",dtype=int)
    XYT = pandas.concat([XY,T],axis=1)
    grouped_by_time = XYT.groupby("time")

    Feature_list = []
    Hull_ext = []

    for t,group in grouped_by_time :
        Hull_int = Hull_ext
        XY = list(group[["stop_lon","stop_lat"]].to_numpy()) + Hull_int

        Hull_ext = [(XY[i][0],XY[i][1]) for i in ConvexHull(XY).vertices]

        Poly = geojson.Polygon([Hull_ext,Hull_int])
        Prop = {}
        if t<len(partitions_sec):
            Prop["isochrone"]="< "+seconds_to_hours(partitions_sec[t])
        else :
            Prop["isochrone"]= "> "+seconds_to_hours(partitions_sec[-1])
        Prop["color"]=palette[t]

        Feature_list.append(geojson.Feature(geometry=Poly, properties=Prop))
    Feature_list.reverse()
    Feature_list.append(geojson.Feature(geometry=geojson.Point((PandaV["stop_lon"][start],PandaV["stop_lat"][start])),properties={"centre":PandaV["station_name"][start]}))
    return geojson.FeatureCollection(Feature_list)

def create_geojson_file(file_path,geojson_feature):
    file = open(file_path,"w")
    file.write("var isochrones = ")
    file.write(geojson.dumps(geojson_feature))
    file.close()
