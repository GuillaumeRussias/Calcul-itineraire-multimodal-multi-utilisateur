from scipy.spatial import ConvexHull
import pandas
import numpy as np
import geojson
import time


partitions_min = np.array([10,20,30,45,60,90,120,180])
partitions_sec = partitions_min*60
palette = ["#0000FF","#FF0000","#FFFF00","#008000","#DC143C","#4682B4","#800000","#1E90FF"]

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
    for t,group in grouped_by_time :
        if t<len(partitions_min):
            Poly = geojson.MultiPoint([(group["stop_lon"][i],group["stop_lat"][i]) for i in group.index])
            Prop = {}
            if t<len(partitions_sec):
                Prop["isochrone"]="< "+seconds_to_hours(partitions_sec[t])
            else :
                Prop["isochrone"]= "> "+seconds_to_hours(partitions_sec[-1])
            Prop["color"]=palette[t%len(palette)]
            Prop["type"]="stop"
            Feature_list.append(geojson.Feature(geometry=Poly, properties=Prop))
    Feature_list.reverse()
    Feature_list.append(geojson.Feature(geometry=geojson.Point((PandaV["stop_lon"][start],PandaV["stop_lat"][start])),properties={"centre":PandaV["station_name"][start],"type":"center"}))
    return geojson.FeatureCollection(Feature_list)

def create_geojson_file(file_path,geojson_feature):
    file = open(file_path,"w")
    file.write("var isochrones = ")
    file.write(geojson.dumps(geojson_feature))
    file.close()
