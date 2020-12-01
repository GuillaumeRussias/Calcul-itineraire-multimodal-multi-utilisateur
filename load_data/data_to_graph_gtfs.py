import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import base_donnee.gtfs_classes as data
import pandas
import numpy as np
import networkx as nx
import datetime
import matplotlib.pyplot as plt

def get_ZDL_from_STOPPOINT(Stop_point):
    """Returns ZDL(IDFM) of a stopPoint (gtfs) """
    ZDL=LINK_GTFS_IDFM.select_lines(column="stop_id", criterion_values=[Stop_point])
    ZDL=ZDL.select_columns(columns=["ZDLr_ID_REF_A"])
    return ZDL.Data_Frame


def dist(v,a):
    V=v.coordinates
    X=a["stop_lon"].to_numpy(float)
    Y=a["stop_lat"].to_numpy(float)
    d=[(X[i]-V[0])**2+(Y[i]-V[1])**2 for i in range (len(X))]
    return d


def get_STOPPOINTS_from_ZDL(ZDL):
    """ Returns all stopPoints(gtfs) from a ZDL(IDFM)"""
    STOPPOINTS=LINK_GTFS_IDFM.select_lines(column="ZDLr_ID_REF_A", criterion_values=[ZDL])
    STOPPOINTS=STOPPOINTS.select_columns(columns=["stop_id","stop_name","stop_lon","stop_lat"])
    return STOPPOINTS.Data_Frame



def create_edges(dfmissions):
    """Create a Pandas DataFrame with edges data """
    dfmissions['route_short_name']=dfmissions['agency_name']+' '+dfmissions['route_short_name']

    Left=dfmissions[["route_short_name","trip_id","departure_time","stop_id","route_id"]]
    Right=dfmissions[["arrival_time","stop_id"]]

    Left_key=dfmissions["trip_id"]+"###"+(dfmissions["stop_sequence"]+1).astype(type("1"))
    Right_key=dfmissions["trip_id"]+"###"+(dfmissions["stop_sequence"]).astype(type("1"))

    Left=pandas.concat([Left, Left_key],axis=1)
    Right=pandas.concat([Right, Right_key],axis=1)

    Left.rename(columns={"stop_id":"departure_stop_id"},inplace=True)
    Left.rename(columns = {'route_short_name':'line_name'}, inplace = True)
    Right.rename(columns={"stop_id":"arrival_stop_id"},inplace=True)

    PandaE=Left.merge(Right,on=0,sort=False)
    PandaE=PandaE[["line_name","trip_id","departure_stop_id","arrival_stop_id","departure_time","arrival_time","route_id"]]

    return PandaE


def create_vertices(PandaE,link):
    """Create a Pandas DataFrame with vertices data """
    link.rename(columns={"stop_id":"gtfs_id"},inplace=True)
    link.rename(columns={"ZDLr_ID_REF_A":"idfm_zdl"},inplace=True)
    link.rename(columns={"stop_name":"station_name"},inplace=True)
    PandaV=link[["gtfs_id","idfm_zdl","station_name","stop_lat","stop_lon"]]
    grouped_e=PandaE.groupby("departure_stop_id")
    L=[]
    for x in PandaV["gtfs_id"]:
        try :
            L.append(grouped_e.get_group(x).index.to_list())
        except KeyError as key:
            print(key,x,"not found in link")
            L.append([])
    edges_index_list=pandas.Series(L,name="edges_index_list")
    PandaV=pandas.concat([PandaV,edges_index_list],axis=1)
    return PandaV

def create_vertice_alt(PandaE,link):
    PandaV = link
    PandaV.rename(columns={"stop_id":"gtfs_id"},inplace=True)
    PandaV.rename(columns={"object_code":"idfm_zde"},inplace=True)
    PandaV.rename(columns={"stop_name":"station_name"},inplace=True)
    PandaV=PandaV[["gtfs_id","idfm_zde","station_name","stop_lat","stop_lon"]]
    grp_edges=PandaE.groupby("departure_stop_id")
    dict={"gtfs_id":[],"edges_index_list":[]}
    for dep_id,edge in grp_edges:
        dict["gtfs_id"].append(dep_id)
        dict["edges_index_list"].append(edge.index.to_list())
    print(len(dict["gtfs_id"]))
    for x in PandaV["gtfs_id"]:
        if x not in dict["gtfs_id"]:
            dict["gtfs_id"].append(x)
            dict["edges_index_list"].append([])

    print(len(dict["gtfs_id"]))
    dict=pandas.DataFrame(dict)

    PandaV=PandaV.merge(dict,on="gtfs_id")
    return PandaV


def get_optimal_vertex(V,List_of_nodes):
    min=np.inf
    vmin=np.inf
    for v in List_of_nodes:
        d = data.distance_metre(v,V)
        if d<min:
            vmin = v
            min = d
    return vmin

def displayable_edges_of_single_fer_line(trace,grp_route,part_PandaE_same_line,PandaV,route_id):
    total_dict={}
    try :
        G=trace.builds_graph_of_single_line(grp_route)
    except KeyError:
        print("no displayable route find",route_id)
        for jndex in part_PandaE_same_line.index:
            total_dict[jndex]=[]
    else :
        #gestion du bug du rerD
        if route_id=="800:D":
            Vdep = get_optimal_vertex((2.439,48.721),G.nodes)
            Varr = get_optimal_vertex((2.446,48.730),G.nodes)
            G.add_edge(Vdep,Varr,weight = 1,index = None)
        #gestion bug de la ligne P:
        if route_id=="800:P":
            Vdep = get_optimal_vertex((2.7272,48.7465),G.nodes)
            Varr = get_optimal_vertex((2.7295,48.7447),G.nodes)
            G.add_edge(Vdep,Varr,weight = 1,index = None)
        for jndex in part_PandaE_same_line.index:
            idep = part_PandaE_same_line["departure_stop_index"][jndex]
            iarr = part_PandaE_same_line["arrival_stop_index"][jndex]
            Vdep = [PandaV["stop_lon"][idep],PandaV["stop_lat"][idep]]
            Varr = [PandaV["stop_lon"][iarr],PandaV["stop_lat"][iarr]]
            Varropt,Vdepopt=get_optimal_vertex(Varr,G.nodes),get_optimal_vertex(Vdep,G.nodes)
            path = nx.shortest_path(G,source=Vdepopt,target=Varropt)
            L=[]
            for i in range (len(path)-1):
                e = G[path[i]][path[i+1]]["index"]
                if e != None :
                    L.append(e)
            total_dict[jndex]=L
    return total_dict

def FER_link_PandaE_with_disp_edges(PandaE,PandaV,color):
    dict={}#dict[index of an edge]=list of index of displayable edges in trace
    trace=data.trace_fer().Data_Frame
    trace=data.trace_fer(copy=data.gtfs(df = trace.merge(color,left_on="extcode",right_on="route_id")))
    grouped=trace.group_by_line() #we regroup displayable edges in group of same lines : ex : RER D, T6, FUN
    for route_id,grp_route in grouped:
        print("traitement Fer",route_id)
        part_PandaE = PandaE[PandaE["route_id"].map(lambda c: c == route_id)]
        dict.update(displayable_edges_of_single_fer_line(trace,grp_route,part_PandaE,PandaV,route_id))
    disp_edge=pandas.Series(dict,name="list_of_disp_edge_index",dtype=object)
    PandaE=pandas.concat([PandaE, disp_edge],axis=1)
    return PandaE,trace.Data_Frame

def BUS_trace_to_graph(Geo_shape):
    G=nx.Graph()
    type = Geo_shape["type"][0]
    Ligne = Geo_shape["coordinates"]
    if type=="LineString":
        for i in range (len(Ligne)-1):
            bool1,v1=data.is_vertice_in_list_based_on_coords_with_epsilon(tuple(Ligne[i]),G.nodes,eps=1)
            bool2,v2=data.is_vertice_in_list_based_on_coords_with_epsilon(tuple(Ligne[i+1]),G.nodes,eps=1)
            G.add_edge(v1,v2)
    else : #=multiLineString
        for subLigne in Ligne :
            for i in range (len(subLigne)-1):
                bool1,v1=data.is_vertice_in_list_based_on_coords_with_epsilon(tuple(subLigne[i]),G.nodes,eps=1)
                bool2,v2=data.is_vertice_in_list_based_on_coords_with_epsilon(tuple(subLigne[i+1]),G.nodes,eps=1)
                G.add_edge(v1,v2)
    return G


def BUS_link_PandaE_with_disp_edges(PandaE,PandaV):
    dict={}#dict[index of an edge]=index in line_to_display
    Line_to_display=[] #list of nodes ->beautifull path
    len_Line_to_display = 0

    ref_lig = data.ref_lig()
    trace = data.trace_bus()
    trace = trace.get_connected_table(ref_lig)
    line_group = PandaE.groupby("route_id")
    for route_id,line in line_group :
        index_ligne_trace = trace[trace["ExternalCode_Line"].map(lambda c: c==route_id)]
        if index_ligne_trace.empty:
            continue
        print("traitement Bus",route_id)
        index_ligne_trace = index_ligne_trace.index[0]
        ligne_trace = trace["Geo Shape"][index_ligne_trace]
        G = BUS_trace_to_graph(ligne_trace)        #construction du graph
        physic_edges = line.groupby(line.apply(lambda c:(c["departure_stop_index"],c["arrival_stop_index"]),axis=1))
        for tuple,physic_edge in physic_edges :
            dep = tuple[0]
            arr = tuple[1]
            Vdep = [PandaV["stop_lon"][dep],PandaV["stop_lat"][dep]]
            Varr = [PandaV["stop_lon"][arr],PandaV["stop_lat"][arr]]
            depopt,arropt=get_optimal_vertex(Vdep,G.nodes),get_optimal_vertex(Varr,G.nodes)
            try :
                path = nx.shortest_path(G,source=depopt,target=arropt)
            except nx.exception.NetworkXNoPath as ex: #path not find , pas tres grave :(
                print(ex)
                path = [Vdep,Varr]
            Line_to_display.append([list(p) for p in path])
            len_Line_to_display += 1
            for jndex in physic_edge.index :
                dict[jndex]= len_Line_to_display - 1
    disp_edge_index=pandas.Series(dict,name="disp_edge_index_bus",dtype=object)
    disp_edge_bus=pandas.Series(Line_to_display,name="Disp_edge_Bus",dtype=object)
    PandaE = pandas.concat([PandaE,disp_edge_index],axis=1)
    print("end traitement bus")
    return  PandaE , disp_edge_bus




def stop_index(PandaE,PandaV):
    grp_edges=PandaE.groupby("departure_stop_id")
    #dict_dep={"index":[],"departure_stop_index":[],"route_id" = []}
    dict_dep={"index":[],"departure_stop_index":[]}
    dict_arr={"index":[],"arrival_stop_index":[]}
    for dep_id,edge in grp_edges:
        f = lambda c : c == dep_id
        try :
            id_v=PandaV[PandaV["gtfs_id"].map(f)].index[0]
        except :
            print(dep_id)
            id_v=None
        dict_dep["index"]+=edge.index.to_list()
        dict_dep["departure_stop_index"]+=[id_v for i in edge.index]
        #dict_dep["route_id"] += edge["route_id"].to_list()
    grp_edges=PandaE.groupby("arrival_stop_id")
    for arr_id,edge in grp_edges:
        f = lambda c : c == arr_id
        try :
            id_v=PandaV[PandaV["gtfs_id"].map(f)].index[0]
        except :
            print(arr_id)
            id_v=None
        dict_arr["index"]+=edge.index.to_list()
        dict_arr["arrival_stop_index"]+=[id_v for i in edge.index]
    stop_index=pandas.DataFrame(dict_dep).merge(pandas.DataFrame(dict_arr),on="index",sort=True)
    return stop_index

def create_transfer_edges(PandaV,transferts):
    grp_edges=transferts.groupby("from_stop_id")
    dict_dep={"index":[],"from_stop_id":[],"min_transfer_time":[]}
    dict_arr={"index":[],"to_stop_id":[]}
    for dep_id,edge in grp_edges:
        f = lambda c : c == dep_id
        try :
            id_v=PandaV[PandaV["gtfs_id"].map(f)].index[0]
        except :
            id_v= -1
        dict_dep["index"]+=edge.index.to_list()
        dict_dep["from_stop_id"]+=[id_v for i in edge.index]
        dict_dep["min_transfer_time"]+=edge["min_transfer_time"].to_list()
    grp_edges=transferts.groupby("to_stop_id")
    for arr_id,edge in grp_edges:
        f = lambda c : c == arr_id
        try :
            id_v=PandaV[PandaV["gtfs_id"].map(f)].index[0]
        except :
            id_v= -1
        dict_arr["index"]+=edge.index.to_list()
        dict_arr["to_stop_id"]+=[id_v for i in edge.index]
    stop_index=pandas.DataFrame(dict_dep).merge(pandas.DataFrame(dict_arr),on="index",sort=True)
    stop_index=stop_index[stop_index["from_stop_id"]!= -1]
    stop_index=stop_index[stop_index["to_stop_id"]!= -1]
    return stop_index[["from_stop_id","to_stop_id","min_transfer_time"]]

def create_pandas_table_fast(link,missions,color):
    missions = missions.Data_Frame
    link = link.Data_Frame
    transferts = data.transfers().Data_Frame
    color = color.Data_Frame
    print("creating edges")
    PandaE = create_edges(missions)
    print("creating vertices")
    PandaV = create_vertice_alt(PandaE,link)
    print("making references")
    Stop_index = stop_index(PandaE,PandaV)
    print("concatenation")
    PandaE = pandas.concat([PandaE,Stop_index],axis=1)
    print("creating transfers")
    transferts = create_transfer_edges(PandaV,transferts)
    print("creating displayable edges")
    PandaE , Pandadisp_edges = FER_link_PandaE_with_disp_edges(PandaE,PandaV,color)
    PandaE , Pandadisp_edge_bus = BUS_link_PandaE_with_disp_edges(PandaE,PandaV)
    Pandadisp_edges.rename(columns={"Geo Shape":"2D_line"},inplace=True)
    return PandaE,PandaV,Pandadisp_edges,transferts , Pandadisp_edge_bus



def create_color(color):
    color = color.Data_Frame
    color["route_short_name"]=color['agency_name']+' '+color['route_short_name']
    color=color[["route_short_name","route_color","route_text_color","route_id"]]
    return color



RAIL_AGENCIES=["RER","TRAIN","TRAM","TRAMWAY","METRO","Navette","SAVAC","SQYBUS"]
BUS = ["SAVAC"]
DATE=datetime.datetime.now()
g_real_name=['T4', 'RER B', 'RER D', 'T2', 'LIGNE R', 'LIGNE H', 'LIGNE P', 'RER C', 'TER', 'T1', 'LIGNE J', 'LIGNE L', 'CDGVAL', 'LIGNE N', 'RER A', 'LIGNE K', 'M8', 'M6', 'M1', 'RER E', 'M9', 'LIGNE U', 'M10', 'M4', 'M12', 'ORLYVAL', 'M13', 'M2', 'M5', 'M7', 'M3bis', 'M3', 'M14', 'M7bis', 'M11', 'T7', 'T8', 'T6', 'T3A', 'T3B', 'T5', 'T11', 'FUNICULAIRE MONTMARTRE']

def Graph_files_creator(agencies=RAIL_AGENCIES,date_creation=DATE,bool_excel=False,bool_pickle=True):
    #pre configuration des datas charges
    print("configuration gtfs data")
    selected_routes=data.get_routes_of_an_agency(line_agencies=agencies)
    missions=data.get_trips_data(Routes=selected_routes,date=date_creation)
    link_gtfs_idfm=data.get_link_gtfs_idfm(stop_times=missions)
    color=data.color_table(Routes=selected_routes)
    print( "end configuration gtfs data")
    #creation des tables :
    print( "creating graph files")
    print("Jour de la semaine : Attention au dimanche ", date_creation.weekday())
    PandaC=create_color(color)
    PandaE,PandaV,PandaDisp_edges,transferts,Pandadisp_edge_bus=create_pandas_table_fast(link=link_gtfs_idfm,missions=missions,color=color)
    #compression avant exportation (suppression champs inutiles)
    PandaE=PandaE[["departure_stop_index","arrival_stop_index","departure_time","arrival_time","route_id","list_of_disp_edge_index","disp_edge_index_bus"]]
    PandaV=PandaV[["gtfs_id","idfm_zde","station_name","stop_lat","stop_lon"]]
    if bool_excel :
        print( "exporting graph files in excel format (very long)")
        PandaE.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_E.xlsx")
        PandaV.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_V.xlsx")
        PandaDisp_edges.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_PandaDispEdges.xlsx")
        PandaC.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_Color.xlsx")
        transferts.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_transferts.xlsx")
        Pandadisp_edge_bus.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_PandaDispEdgesBus.xlsx")
    if bool_pickle:
        print( "exporting graph files in pickle format")
        PandaE.to_pickle(parentdir+"/base_donnee/datas/graph_files/gtfs_E.pkl")
        PandaV.to_pickle(parentdir+"/base_donnee/datas/graph_files/gtfs_V.pkl")
        PandaDisp_edges.to_pickle(parentdir+"/base_donnee/datas/graph_files/gtfs_PandaDispEdges.pkl")
        PandaC.to_pickle(parentdir+"/base_donnee/datas/graph_files/gtfs_Color.pkl")
        transferts.to_pickle(parentdir+"/base_donnee/datas/graph_files/gtfs_transferts.pkl")
        Pandadisp_edge_bus.to_pickle(parentdir+"/base_donnee/datas/graph_files/gtfs_PandaDispEdgesBus.pkl")
    print("exporting station name in excel format")
    PandaV = PandaV["station_name"]
    PandaV.to_excel(parentdir+"/base_donnee/datas/graph_files/station_name.xlsx")

Graph_files_creator(agencies=["ALL"])
temps_exec=datetime.datetime.now()
print(temps_exec-DATE)
