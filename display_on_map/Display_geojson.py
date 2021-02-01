import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from display_on_map.Display_compiled import *
import geojson
import folium
import folium.plugins



def idfm_to_geojson_coords(list2D):
    to_return=[]
    for v in list2D:
        to_return.append((v[0],v[1]))
    return to_return

def to_geojson_station(features_list,Coords,Name,Color,Ligne):
    point = geojson.Point((Coords[0],Coords[1]))
    properties = { "color" : Color ,"name" : Name , "route_name" : Ligne }
    features_list.append(geojson.Feature(geometry=point,properties=properties))

def to_geojson_Multiline(features_list,MultiLine,metadata):
    MultiLineString = geojson.MultiLineString(MultiLine)
    #f"""Ligne : {metadata["route_name"]} , Direction : {metadata["trip_headsign"]} , Station de départ : {metadata["departure_name"]} à {metadata["departure_time"]}, Station d'arrivée : {metadata["arrival_name"]} à {metadata["arrival_time"]} , ({len(MultiLine)} Stations(s))"""}
    metadata["len"] = len(MultiLine)
    features_list.append(geojson.Feature(geometry=MultiLineString,properties=metadata))

def edge_metadata_geojson(edge_id,EdgeData,LineData,edge_type,departure_name,arrival_name,departure_time,arrival_time):
    metadata={}
    if edge_id != -1 :
        route_id= EdgeData["route_id"][edge_id]
        selected_line = LineData[LineData["route_id"].map(lambda c:c==route_id)].index[0]
        metadata["route_name"] = LineData["route_short_name"][selected_line]
        metadata["route_color"] = "#" + LineData["route_color"][selected_line]
        metadata["route_text_color"] = "#" + LineData["route_text_color"][selected_line]
        metadata["trip_headsign"] =  EdgeData["trip_headsign"][edge_id]
        metadata["departure_time"] = seconds_to_hours(departure_time)
        metadata["arrival_time"] = seconds_to_hours(arrival_time)

    else :
        metadata["route_name"] = "Connection multimodale"
        metadata["route_color"] = "#708090"
        metadata["route_text_color"] = "#000000"
        metadata["departure_time"] = ""
        metadata["arrival_time"] = seconds_to_hours(arrival_time)
        metadata["trip_headsign"] = ""

    metadata["departure_name"] = departure_name
    metadata["arrival_name"] = arrival_name


    return metadata

def fill_geometry(start_coords,end_coords,Display,edgeDisplay_index) :
    physical_track , extrems = [],[]
    if edgeDisplay_index != None : #scheduled edge
        physical_track = idfm_to_geojson_coords(Display[edgeDisplay_index])
    else : #free edge
        physical_track = [(start_coords[0],start_coords[1]),(end_coords[0],end_coords[1])]
    extrems = [start_coords,end_coords]
    return physical_track , extrems

def geojson_edge(Point_list,MultiLine_list, VertexData, EdgeData , Display, LineData , CompiledGraph , precedent_vertex_index , vertex_index, last , previous_metadata , MultiLine):
    edge = CompiledGraph[precedent_vertex_index][vertex_index]
    edge_id = edge.id()
    time_departure , time_arrival = edge.selected_mission()
    edge_type = edge.type()

    start_coords = np.array([VertexData["stop_lon"][precedent_vertex_index],VertexData["stop_lat"][precedent_vertex_index]])
    end_coords = np.array([VertexData["stop_lon"][vertex_index],VertexData["stop_lat"][vertex_index]])
    start_name = VertexData["station_name"][precedent_vertex_index]
    end_name = VertexData["station_name"][vertex_index]

    edgeDisplay_index = None
    if edge_id != -1:
        edgeDisplay_index = EdgeData["disp_edge_index"][edge_id]

    physical_track , extrems = fill_geometry(start_coords,end_coords,Display,edgeDisplay_index)
    metadata = edge_metadata_geojson(edge_id,EdgeData,LineData,edge_type,start_name,end_name,time_departure,time_arrival)

    previous_line = previous_metadata["route_name"] + previous_metadata["trip_headsign"]
    current_line = metadata["route_name"] + metadata["trip_headsign"]

    if previous_line == current_line :
        MultiLine.append(physical_track)
        metadata["departure_time"] = previous_metadata["departure_time"]
        metadata["departure_name"] = previous_metadata["departure_name"]
    elif previous_line != "" :
        to_geojson_Multiline(MultiLine_list,MultiLine,previous_metadata)
        MultiLine.clear()
        MultiLine.append(physical_track)
    else:
        MultiLine.append(physical_track)

    previous_metadata = metadata

    if last == False :
        to_geojson_station(Point_list,extrems[0],start_name,metadata["route_color"],metadata["route_name"])
    if last == True :
        to_geojson_station(Point_list,extrems[1],end_name,metadata["route_color"],metadata["route_name"])
        to_geojson_Multiline(MultiLine_list,MultiLine,previous_metadata)

    return previous_metadata

def geojson_traject(VertexData , EdgeData, Display, LineData , Path , CompiledGraph):
    Point_list = []
    MultiLine_list = []
    MultiLine = []
    precedent_vertex_index = Path[0]
    previous_metadata = {"route_name":"","trip_headsign":""}
    for vertex_index in Path[1:] :
        previous_metadata = geojson_edge(Point_list,MultiLine_list, VertexData, EdgeData , Display, LineData , CompiledGraph , precedent_vertex_index , vertex_index, False, previous_metadata , MultiLine)
        precedent_vertex_index = vertex_index
    if len(Path)>1:
        geojson_edge(Point_list,MultiLine_list, VertexData, EdgeData , Display, LineData , CompiledGraph , Path[-2] , Path[-1], True , previous_metadata , MultiLine)
    return geojson.FeatureCollection(MultiLine_list+Point_list)


def style_point(feature,bool_highlight):
    return {
    "color" : feature["properties"]["color"],
    "fillColor": "#ffffff",
    "radius" : radius*(int(bool_highlight)+1),
    }

def style_MultiLine(feature,bool_highlight):
    return{
    "color" : feature["properties"]["route_color"],
    "weight" : weight*(int(bool_highlight)+1),
    }

def style_feature(feature,bool_highlight):
    #print(feature)
    if feature["geometry"]["type"]=="Point" :
        return style_point(feature,bool_highlight)
    else :
        return style_MultiLine(feature,bool_highlight)


def map_from_geojson(geojson_features, map , css_style_tool = None , css_style_popup = None):
    geo = folium.GeoJson(
    geojson_features,
    style_function = lambda feature: style_feature(feature,False),
    highlight_function = lambda feature: style_feature(feature,True),
    tooltip =  folium.GeoJsonTooltip(["route_name"],labels=False, style=css_style_tool ,localize=True),
    popup = folium.GeoJsonPopup(fields=["route_name","trip_headsign","departure_name","departure_time","arrival_name","arrival_time","len"],aliases=["Ligne","Direction","Station de départ","à","Station d'arrivée","à","Nombre d'arrêts"], style=css_style_popup,localize=True),
    ).add_to(map)
    folium.plugins.Fullscreen().add_to(map)
    map.get_root().html.save("Folium.html")
    return map

def create_geojson_file(VertexData , EdgeData, Display, LineData , Path , CompiledGraph, file_path):
    geo_features = geojson.dumps(geojson_traject(VertexData , EdgeData, Display, LineData , Path , CompiledGraph))
    file = open(file_path,"w")
    file.write("var traject = ")
    file.write(geo_features)
    file.close()

def create_geojson_traject(VertexData , EdgeData, Display, LineData , Path , CompiledGraph):
    return geojson.dumps(geojson_traject(VertexData , EdgeData, Display, LineData , Path , CompiledGraph))
