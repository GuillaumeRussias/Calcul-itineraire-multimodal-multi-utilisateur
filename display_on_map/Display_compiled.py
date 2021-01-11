import folium
import time
import numpy as np


radius = 50/10
weight = 4



def seconds_to_hours(sec):
    ty_res = time.gmtime(sec)
    res = time.strftime("%H:%M:%S",ty_res)
    return res

def idfm_to_folium_coords(list2D):
    for v in list2D:
        v[0],v[1]=v[1],v[0]
    return list2D

def draw_station(FoliumMap,Coords,Name,Color):
    folium.Circle(radius=radius,location=Coords,popup=Name,color=Color,fill_color=Color,fill_opacity=1,fill=True).add_to(FoliumMap)
    folium.Circle(radius=radius-20,location=Coords,popup=Name,color="WHITE",fill_color="WHITE",fill_opacity=1,fill=True).add_to(FoliumMap)
    return FoliumMap

def draw_line(FoliumMap,physical_track,metadata):
    folium.PolyLine(physical_track,color=metadata["route_color"],weight=weight,popup=metadata["route_name"]+metadata["route_decription"],opacity=1).add_to(FoliumMap)
    return FoliumMap

def edge_metadata2(edge_id,EdgeData,LineData,edge_type,departure_name,arrival_name,departure_time,arrival_time):
    metadata={}
    if edge_id != -1 :
        route_id= EdgeData["route_id"][edge_id]
        selected_line = LineData[LineData["route_id"].map(lambda c:c==route_id)].index[0]
        metadata["route_name"] = LineData["route_short_name"][selected_line]
        metadata["route_color"] = "#" + LineData["route_color"][selected_line]
        metadata["trip_headsign"] =  EdgeData["trip_headsign"][edge_id]
        metadata["route_decription"] = " - " +metadata["trip_headsign"]+ " - " +seconds_to_hours(departure_time) + " - " + seconds_to_hours(arrival_time)
    else :
        metadata["route_name"] = "Multimodal transfer"
        metadata["route_color"] = "grey"
        metadata["route_decription"] = " transfer time : " + seconds_to_hours(arrival_time)
    return metadata


def fill_display2(start_coords,end_coords,Display,edgeDisplay_index) :
    physical_track , extrems = [],[]
    if edgeDisplay_index != None : #scheduled edge
        physical_track = idfm_to_folium_coords(Display[edgeDisplay_index])
    else : #free edge
        physical_track = [start_coords,end_coords]
    extrems = [start_coords,end_coords]
    return physical_track , extrems



def plot_edge2(FoliumMap, VertexData, EdgeData , Display, LineData , CompiledGraph , precedent_vertex_index , vertex_index):
    edge = CompiledGraph[precedent_vertex_index][vertex_index]
    #edge.print_missions()
    edge_id = edge.id()
    time_departure , time_arrival = edge.selected_mission()
    edge_type = edge.type()
    start_coords = np.array([VertexData["stop_lat"][precedent_vertex_index],VertexData["stop_lon"][precedent_vertex_index]])
    end_coords = np.array([VertexData["stop_lat"][vertex_index],VertexData["stop_lon"][vertex_index]])
    start_name = VertexData["station_name"][precedent_vertex_index]
    end_name = VertexData["station_name"][vertex_index]
    edgeDisplay_index = None
    if edge_id != -1:
        edgeDisplay_index = EdgeData["disp_edge_index"][edge_id]
    physical_track , extrems = fill_display2(start_coords,end_coords,Display,edgeDisplay_index)
    metadata = edge_metadata2(edge_id,EdgeData,LineData,edge_type,start_name,end_name,time_departure,time_arrival)
    FoliumMap = draw_line(FoliumMap,physical_track,metadata)
    FoliumMap = draw_station(FoliumMap,extrems[0],start_name,metadata["route_color"])
    FoliumMap = draw_station(FoliumMap,extrems[1],end_name,metadata["route_color"])
    return FoliumMap


def plot_traject2(FoliumMap, VertexData , EdgeData, Display, LineData , Path , CompiledGraph ):
    precedent_vertex_index = Path[0]
    for vertex_index in Path[1:] :
        FoliumMap = plot_edge2(FoliumMap, VertexData, EdgeData , Display, LineData , CompiledGraph , precedent_vertex_index , vertex_index)
        precedent_vertex_index = vertex_index
    return FoliumMap
