import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import base_donnee.gtfs_classes as data
import pandas
import numpy as np
import networkx as nx
import datetime


def create_scheduled_edges(dfmissions):
    """Create a Pandas DataFrame for edges : ["line_name","trip_id","departure_stop_id","arrival_stop_id","departure_time","arrival_time","route_id","trip_headsign"]
    argument : dfmissions is a pandas dataframe with at least columns : ["agency_name","route_short_name","trip_id","arrival_time","departure_time","stop_id","stop_sequence","route_id","trip_headsign"]
    equivalent of gtfs stop_times.txt.
    """
    dfmissions['route_short_name']=dfmissions['agency_name']+' '+dfmissions['route_short_name'] #we create a new name from agency name + route_short_name . exemple : agency = RER route_short_name = B -> route_short_name = RER B

    #we create two tables wich will be merged later in order to create Pandas Dataframe for edge.
    Left=dfmissions[["route_short_name","trip_id","departure_time","stop_id","route_id","trip_headsign"]]
    Right=dfmissions[["arrival_time","stop_id"]]

    #keys for merge
    Left_key=dfmissions["trip_id"]+"###"+(dfmissions["stop_sequence"]+1).astype(type("1"))
    Right_key=dfmissions["trip_id"]+"###"+(dfmissions["stop_sequence"]).astype(type("1"))

    Left=pandas.concat([Left, Left_key],axis=1)
    Right=pandas.concat([Right, Right_key],axis=1)

    Left.rename(columns={"stop_id":"departure_stop_id"},inplace=True)
    Left.rename(columns = {'route_short_name':'line_name'}, inplace = True)
    Right.rename(columns={"stop_id":"arrival_stop_id"},inplace=True)
    #merge operation
    PandaE=Left.merge(Right,on=0,sort=False)
    PandaE=PandaE[["line_name","trip_id","departure_stop_id","arrival_stop_id","departure_time","arrival_time","route_id","trip_headsign"]]

    return PandaE

def create_free_edges():
    """Create a panda dataframe with columns [["from_stop_id","to_stop_id","min_transfer_time"]] """
    free_edges = transferts = data.transfers().Data_Frame
    free_edges.rename(columns = {"from_stop_id":'departure_stop_id'}, inplace = True)
    free_edges.rename(columns=  {"to_stop_id":"arrival_stop_id"}, inplace = True)
    return free_edges[["departure_stop_id","arrival_stop_id","min_transfer_time"]]

def create_vertices(dflink,dfmissions):
    """Create a Pandas DataFrame for vertices : ["gtfs_id","idfm_zde","station_name","stop_lat","stop_lon"]
    arguments :  -dflink is a pandas dataframe with at least columns : ["stop_id","object_code","stop_name","stop_lat","stop_lon"]
                 -dfmissions a pandas dataframe with at least columns : ["stop_id"]
    """
    PandaV = dfmissions.drop_duplicates("stop_id")
    PandaV = PandaV.merge(dflink,on="stop_id")
    PandaV.rename(columns={"stop_id":"gtfs_id"},inplace=True)
    PandaV.rename(columns={"object_code":"idfm_zde"},inplace=True)
    PandaV.rename(columns={"stop_name":"station_name"},inplace=True)
    PandaV = PandaV[["gtfs_id","idfm_zde","station_name","stop_lat","stop_lon"]]
    return PandaV


def link_edges_with_vertices(Edges,PandaV,columns_to_select):
    """
    add columns [departure_stop_index,arrival_stop_index] to PandaE
    arguments :
    Edges : results of create_scheduled_edges or create_free_edges
    PandaV : results of create_vertices
    columns_to_select : list of columns name to select
    """
    index = pandas.Series(PandaV.index.to_list(),name="index")
    stop_id_index = (pandas.concat([PandaV,index],axis = 1))[["gtfs_id","index"]]
    Edges = Edges.merge(stop_id_index,left_on = "departure_stop_id" , right_on = "gtfs_id")
    Edges.rename(columns={"index":"departure_stop_index"},inplace=True)
    Edges = Edges.merge(stop_id_index,left_on = "arrival_stop_id" , right_on = "gtfs_id")
    Edges.rename(columns={"index":"arrival_stop_index"},inplace=True)
    return Edges[columns_to_select]

def create_color(color):
    """Create a table of information about every lines """
    color["route_short_name"]=color['agency_name']+'####'+color['route_short_name']
    color=color[["route_short_name","route_color","route_text_color","route_id"]]
    return color


def get_optimal_vertex(V,List_of_nodes, dmin = 300 ** 2):
    min=np.inf
    vmin=np.inf
    for v in List_of_nodes:
        d = data.distance_metre(v,V)
        if d<min:
            vmin = v
            min = d
    if min>dmin:
        vmin=V
    return vmin


def link_PandaE_with_disp_edges(PandaE,PandaV,bool_skip):
    """Create a Pandas DataSerie with column =["displayable_edges"]. each line contains the shape of an edge of francilain network. Also add ant integer column to PandaE which gives the line of appropriate shape. """
    print("Traitement de l'affichage")

    dict_link_with_disp_edges = {}  #dict[index of an edge]=index in line_to_display
    displayable_edges = []          #list of nodes ->beautifull path
    len_displayable_edges = 0


    referenciel_des_lignes = data.ref_lig()
    trace_bus = data.trace_bus()
    trace_fer = data.trace_fer2()

    trace_fer_grouped_by_line = trace_fer.group_by_line()
    trace_bus_connected = trace_bus.get_connected_table(referenciel_des_lignes)

    edges_grouped_by_line = PandaE.groupby("route_id")


    for route_id,edge_of_single_line in edges_grouped_by_line :
        if bool_skip == False :
            try :
                group_fer = trace_fer_grouped_by_line.get_group(route_id)
                is_line_displayable_fer = True
            except KeyError :
                #cette ligne ne possède pas de trace physique renseigne dans le trace du reseaux ferre d'idf
                is_line_displayable_fer = False
            try :
                index_bus = trace_bus_connected[trace_bus_connected["ExternalCode_Line"].map(lambda c: c==route_id)].index[0]
                is_line_bus_displayable = True
            except IndexError :
                #cette ligne ne possède pas de trace physique renseigne dans le trace du reseaux bus d'idf
                is_line_bus_displayable = False

            if is_line_bus_displayable==False and is_line_displayable_fer == False :
                print("Cette ligne "+route_id+" ne possede pas de trace physique renseigne ni dans le trace du reseaux ferre d'idf ni dans le trace du reseaux bus d'ifm")
                G = nx.Graph()

            if is_line_bus_displayable :
                print("traitement Bus",route_id)
                G = trace_bus.builds_graph_of_single_line(trace_bus_connected,index_bus)

            if is_line_displayable_fer :
                print("traitement Fer",route_id)
                G = trace_fer.builds_graph_of_single_line(group_fer)

        if bool_skip == True :
                G = nx.Graph()

        edges_grouped_by_start_and_end = edge_of_single_line.groupby(edge_of_single_line.apply(lambda c:(c["departure_stop_index"],c["arrival_stop_index"]),axis=1))

        for start_end_index_tuple,edge_of_single_start_and_end in edges_grouped_by_start_and_end :
            dep = start_end_index_tuple[0]
            arr = start_end_index_tuple[1]
            Vdep = [PandaV["stop_lon"][dep],PandaV["stop_lat"][dep]]
            Varr = [PandaV["stop_lon"][arr],PandaV["stop_lat"][arr]]
            depopt,arropt=get_optimal_vertex(Vdep,G.nodes),get_optimal_vertex(Varr,G.nodes)
            try :
                path = nx.shortest_path(G,source=depopt,target=arropt)
            except nx.exception.NetworkXNoPath as ex: #path not find , pas tres grave :(
                print(ex)
                path = []
            except nx.exception.NodeNotFound as ex: #correspond au cas ou is_line_bus_displayable==False and is_line_displayable_fer == False ou bool_skip == True. Ou au cas ou l'arret n'est pas renseigne dans ces bases (trop loin du point de l'optimal)
                path = []
            displayable_edges.append([Vdep]+[list(p) for p in path]+[Varr])
            len_displayable_edges += 1
            for j in edge_of_single_start_and_end.index :
                dict_link_with_disp_edges[j] = len_displayable_edges - 1

    link_with_disp_edges = pandas.Series(dict_link_with_disp_edges,name="disp_edge_index",dtype=int)
    displayable_edges = pandas.Series(displayable_edges,name="displayable_edges",dtype=object)
    PandaE = pandas.concat([PandaE,link_with_disp_edges],axis=1)
    print("Fin Traitement de l'affichage")
    return  PandaE , displayable_edges







def Graph_files_creator(agencies,date_creation,bool_excel = False,bool_pickle = True, bool_skip_disp_edge = False):
    """Creates graph files from gtfs files """
    #pre configuration des datas charges
    print("configuration gtfs data")
    selected_routes = data.get_routes_of_an_agency(line_agencies=agencies)
    missions = data.get_trips_data(Routes=selected_routes,date=date_creation)
    link_gtfs_idfm = data.get_link_gtfs_idfm(stop_times=missions)
    color = data.color_table(Routes=selected_routes)
    print( "end configuration gtfs data")
    #creation des tables :
    print( "creating graph files")

    PandaC = create_color(color.Data_Frame)
    PandaV = create_vertices(dflink = link_gtfs_idfm.Data_Frame , dfmissions = missions.Data_Frame)
    PandaE = create_scheduled_edges (dfmissions = missions.Data_Frame)
    PandaEf = create_free_edges ()
    PandaE = link_edges_with_vertices(PandaE,PandaV,["route_id","trip_headsign","departure_stop_index","arrival_stop_index","departure_time","arrival_time"])
    PandaEf = link_edges_with_vertices(PandaEf,PandaV,["departure_stop_index","arrival_stop_index","min_transfer_time"])
    PandaE , PandaDisp = link_PandaE_with_disp_edges(PandaE,PandaV,bool_skip_disp_edge)

    #compression avant exportation (suppression champs inutiles)
    if bool_excel :
        print( "exporting graph files in excel format (very long)")
        PandaE.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_E.xlsx")
        PandaV.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_V.xlsx")
        PandaC.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_Color.xlsx")
        PandaEf.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_Ef.xlsx")
        PandaDisp.to_excel(parentdir+"/base_donnee/datas/graph_files/gtfs_Disp.xlsx")

    if bool_pickle :
        print( "exporting graph files in pickle format")
        PandaE.to_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_E.pkl")
        PandaV.to_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_V.pkl")
        PandaDisp.to_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_PandaDisp.pkl")
        PandaC.to_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_Color.pkl")
        PandaEf.to_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_Ef.pkl")

    print("exporting station name in excel format")
    PandaV["station_name"] = PandaV["station_name"] + " / " + PandaV.index.map(str)
    PandaV = PandaV["station_name"]
    PandaV.to_excel(parentdir+"/base_donnee/datas/graph_files/station_name.xlsx")
    PandaV.to_pickle(parentdir+"/base_donnee/datas/graph_files/station_name.pkl")

Graph_files_creator(["ALL"],datetime.datetime.now())
#Graph_files_creator(["METRO"],datetime.datetime.now())
