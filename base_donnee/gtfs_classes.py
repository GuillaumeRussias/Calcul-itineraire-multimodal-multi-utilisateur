import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import pandas
import datetime
import numpy as np
import networkx as nx
import requests

import base_donnee.downloader as downloader



class gtfs:
    """A class with basic methods to deal with gtfs files . Use pandas """
    def __init__(self,df=None,adress=None,low_memory=True,separator=',',engine=None):
        """ constructor : create a gtfs from an adress or a dataframe"""
        if adress==None and type(df)!=type(None):
            #appel du constructeur a partir de df
            self.Data_Frame=df
        elif adress!=None and type(df)==type(None):
            #appel constructeur a partir fichier
            if engine==None :
                self.Data_Frame=pandas.read_csv(adress,low_memory=low_memory,sep=separator)
            else :
                self.Data_Frame=pandas.read_csv(adress,sep=separator,engine=engine)
        else :
            raise AttributeError("Erreur constructeur, il faut préciser en argument soit df (un data frame pandas) soit adress (l'adress d'un fichier csv) mais pas les deux ni aucun")

    def select_lines(self, column , criterion_values ):
        """select lines from self.Data_Frame where column satisfies criterion_values"""
        if type(criterion_values)==type([]):
            criterion = self.Data_Frame[column].map(lambda c: c in criterion_values)
            return gtfs(df=(self.Data_Frame[criterion]))
        else :
            criterion = self.Data_Frame[column].map(lambda c: c == criterion_values)
            return gtfs(df=(self.Data_Frame[criterion]))

    def select_lines_on_function(self, column , bool_function ):
        """select lines from self.Data_Frame where column satisfies bool_function"""
        criterion = self.Data_Frame[column].map(bool_function)
        return gtfs(df=(self.Data_Frame[criterion]))

    def select_columns(self, columns):
        """select indicated columns """
        return gtfs(df=(self.Data_Frame[columns]))

    def display(self):
        """print Data_Frame """
        print(self.Data_Frame)

    def merge(self,other,key):
        """Requete SQL : Select * from self Join other on key"""
        return gtfs(df=(pandas.merge(self.Data_Frame,other.Data_Frame,on=key,sort=False)))

    def merge_double_key(self,other,key_self,key_other):
        """Requete SQL : Select * from self Join other on key_self=key_other"""
        return gtfs(df=(pandas.merge(self.Data_Frame,other.Data_Frame, left_on=key_self, right_on=key_other,sort=False)))

    def drop_duplicates(self,columns):
        """enleve les doublons """
        return gtfs(df=(self.Data_Frame.drop_duplicates(subset=columns)))

    def convert_column_type(self,column,type=type(1)):
        """convertit le type de la colonne column dans le type donne """
        self.Data_Frame[column]=self.Data_Frame[column].astype(type)

    def sort(self,column):
        """ sort a dataframe by column value"""
        return gtfs(df=(self.Data_Frame.sort_values(by=column)))

    def clean(self,Columns_to_select):
        """select Columns_to_select from the dataframe """
        return self.select_columns(Columns_to_select)



def import_gtfs(ADRESS):
    """ load in DATA dictionnary all gtfs and idfm files"""
    DATA={
    "agency":gtfs(adress=ADRESS["agency"]),
    "calendar_dates":gtfs(adress=ADRESS["calendar_dates"]),
    "calendar":gtfs(adress=ADRESS["calendar"]),
    "routes":gtfs(adress=ADRESS["routes"]),
    "stop_times":gtfs(adress=ADRESS["stop_times"]),
    "stops":gtfs(adress=ADRESS["stops"]),
    "transfers":gtfs(adress=ADRESS["transfers"]),
    "trips":gtfs(adress=ADRESS["trips"],low_memory=False),
    }
    try :
        DATA["trace_fer"]=gtfs(adress=ADRESS["trace_fer"],separator=";")
        DATA["trace_bus"]=gtfs(adress=ADRESS["trace_bus"],separator=";")
        DATA["ref_lig"]=gtfs(adress=ADRESS["ref_lig"],separator=";")
        DATA["stop_extensions"]=gtfs(adress=ADRESS["stop_extensions"])
    except :
        print("une erreur est detectee dans l'importation des bases non essentielles")
        DATA["trace_fer"]=gtfs(df=pandas.DataFrame())
        DATA["trace_bus"]=gtfs(df=pandas.DataFrame())
        DATA["ref_lig"]=gtfs(df=pandas.DataFrame())
        DATA["stop_extensions"]=gtfs(df=pandas.DataFrame())
    try :
        DATA["reflex"]= gtfs(adress=ADRESS["reflex"],separator="|")
    except :
        print("erreur reflex fichier corrompu")
        DATA["reflex"]= gtfs(df=pandas.DataFrame())

    return DATA


print("Importing gtfs datas")
bool_other_data = False #NYC
bool_gtfs = input("Do you want to (re-)download gtfs ? y/n ")=="y"
#succes = downloader.download_check(downloader.force_download(gtfs=bool_gtfs,ref_lig=bool_gtfs,trace=False,reflex=False))
if bool_other_data==False :
    succes = downloader.download_check(downloader.force_download(gtfs=bool_gtfs,ref_lig=bool_gtfs,trace=bool_gtfs,reflex=bool_gtfs))
if succes == False :
    print("Download Failure")
    exit(2)
print("Download Succes")
DATA = import_gtfs(downloader.ADRESS)
print("import done")





class stop_times(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["stop_times"]):
        super().__init__(df=copy.Data_Frame)

    def get_trip(self,trip_id):
        return self.select_lines(column="trip_id",criterion_values=[trip_id]).sort(column="stop_sequence")

class agency(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["agency"]):
        super().__init__(df=copy.Data_Frame)

class routes(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["routes"]):
        super().__init__(df=copy.Data_Frame)

    def select_route_on_name(self,route_short_name):
        """selecting a route on name : WARNING possible ambiguity if multiple routes share same short name"""
        if type(route_short_name)==type([]):
            return self.select_lines(column="route_short_name",criterion_values=route_short_name)
        else:
            return self.select_lines(column="route_short_name",criterion_values=[route_short_name])

class trips(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["trips"]):
        super().__init__(df=copy.Data_Frame)

class stops(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["stops"]):
        super().__init__(df=copy.Data_Frame)

class stop_extensions(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["stop_extensions"]):
        super().__init__(df=copy.Data_Frame)

    def merge_with_stop(self,stops):
        a=self.merge_double_key(stops,"object_id","stop_id")
        a=a.select_lines("object_system",["ZDEr_ID_REF_A","source"])
        return a

class reflex(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["reflex"]):
        super().__init__(df=copy.Data_Frame)
    def merge_with_stop_extensions(self,stop_extensions):
        a=self.merge_double_key(stop_extensions,'ZDEr_ID_REF_A','object_code')
        return a

class transfers(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["transfers"]):
        super().__init__(df=copy.Data_Frame)

class calendar(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["calendar"],date=None):
        super().__init__(df=copy.Data_Frame)
        assert (date!=None ), "no date given in calendar"
        calendar.date = date
        calendar.dateint = calendar.date_gtfs(date)
        print(calendar.dateint)
    def day_gtfs(date):
        days=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        return days[date.weekday()]
    def date_gtfs(date):
        AAAAMMJJ=str(date.year)+("0"*(date.month<10))+str(date.month)+("0"*(date.day<10))+str(date.day)
        return int(AAAAMMJJ)
    def start_date(c):
        return int(c)<=calendar.dateint
    def end_date(c):
        return int(c)>=calendar.dateint
    def select_online_services(self):
        online=self.select_lines(column=calendar.day_gtfs(calendar.date) ,criterion_values= [1])
        online=online.select_lines_on_function('start_date',calendar.start_date)
        online=online.select_lines_on_function('end_date',calendar.end_date)
        return online

class calendar_dates(gtfs):
    """ daughter class of gtfs deals with gtfs file of the same name """
    def __init__(self,copy=DATA["calendar_dates"],date=None):
        super().__init__(df=copy.Data_Frame)
        assert (date!=None ), "no date given in calendar_date"
        calendar_dates.dateint = calendar.date_gtfs(date)

    def select_online_services(self):
        online=self.select_lines(column="date",criterion_values = calendar_dates.dateint)
        return online




def distance_metre(v1,v2):
    #conversion
    x1 , x2 = v1[0]*73340 , v2[0]*73340
    y1 , y2 = v1[1]*111300 , v2[1]*111300
    d = (x1-x2)**2 + (y1-y2)**2
    return d

def is_vertice_in_list_based_on_coords_with_epsilon(v,l,eps=10*2):
    min=np.inf
    vmin=np.inf
    for m in l : #calcul distance minimale
        d = distance_metre(m,v)
        if d<min:
            min=d
            vmin=m
    if min <= eps : #si cette distance est inferieure a epsilon, on considere que v appartient a
        return True,vmin
    return False,v



def add_edges_graph_from_geo_shape(G,Geo_shape):
    type = Geo_shape["type"][0]
    Ligne = Geo_shape["coordinates"]
    if type=="LineString":
        for i in range (len(Ligne)-1):
            bool1,v1=is_vertice_in_list_based_on_coords_with_epsilon(tuple(Ligne[i]),G.nodes,eps=10)
            bool2,v2=is_vertice_in_list_based_on_coords_with_epsilon(tuple(Ligne[i+1]),G.nodes,eps=10)
            G.add_edge(v1,v2)
    else : #=multiLineString
        for subLigne in Ligne :
            for i in range (len(subLigne)-1):
                bool1,v1=is_vertice_in_list_based_on_coords_with_epsilon(tuple(subLigne[i]),G.nodes,eps=10)
                bool2,v2=is_vertice_in_list_based_on_coords_with_epsilon(tuple(subLigne[i+1]),G.nodes,eps=10)
                G.add_edge(v1,v2)
    return G



class trace_fer2(gtfs):
    """ a class dealing with the shape of rail lines"""
    def __init__(self,copy=DATA["trace_fer"]):
        super().__init__(df=copy.Data_Frame)

    def group_by_line(self):
        pandas.set_option('mode.chained_assignment', None)
        self.Data_Frame=self.Data_Frame[["Geo Shape","id_fmt_tem","OBJECTID","extcode"]]
        self.Data_Frame['Geo Shape']=self.Data_Frame['Geo Shape'].map(lambda c:pandas.read_json(c))
        pandas.set_option('mode.chained_assignment', 'warn')
        return self.Data_Frame.groupby("extcode")

    def builds_graph_of_single_line(self,grp_route):
        if grp_route.empty:
            raise KeyError("empty dataframe after research on route_id")
        G = nx.Graph()
        for i in grp_route.index :
            Geo_shape = grp_route["Geo Shape"][i]
            G = add_edges_graph_from_geo_shape(G,Geo_shape)
        return G

class ref_lig(gtfs):
    """ a class dealing with line referential"""
    def __init__(self,copy=DATA["ref_lig"]):
        super().__init__(df=copy.Data_Frame)

class trace_bus(gtfs):
    """ a class dealing with the shape of bus lines"""
    def __init__(self,copy=DATA["trace_bus"]):
        super().__init__(df=copy.Data_Frame)

    def get_connected_table(self,ref_lig):
        self = self.merge(ref_lig,key="ID_GroupOfLines")
        self = self.select_columns(columns=["ExternalCode_Line","Geo Shape"])
        self.Data_Frame["Geo Shape"] = self.Data_Frame["Geo Shape"].map(lambda c : pandas.read_json(c))
        return self.Data_Frame

    def builds_graph_of_single_line(self,grp_route,index_route):
        G = nx.Graph()
        Geo_shape = grp_route["Geo Shape"][index_route]
        G = add_edges_graph_from_geo_shape(G,Geo_shape)
        return G



def get_routes_of_an_agency(line_agencies=["RER"]):
    """ select routes of line_agencies : returns routes gtfs dataframe with ["agency_id","route_short_name","route_id","route_color","route_text_color"] columns """
    Agency=agency()
    Agency=Agency.clean(Columns_to_select=["agency_id","agency_name"])
    if line_agencies[0]!="ALL" :
        Agency=Agency.select_lines(column="agency_name",criterion_values=line_agencies)

    Routes=routes()
    Routes=Routes.clean(Columns_to_select=["agency_id","route_short_name","route_id","route_color","route_text_color"])
    Routes=Routes.merge(Agency,key="agency_id")
    return Routes


def get_trips_data(Routes,date):
    """ From a date and a route gtfs dataframe containing at least columns ["agency_id","route_short_name","route_id","route_color","route_text_color"] , returns a stop_times gtfs dataframe
    with columns ["agency_name","route_short_name","trip_id","start_date","end_date","arrival_time","departure_time","stop_id","stop_sequence","route_id","trip_headsign"]"""
    Trips=trips()
    Trips=Trips.clean(Columns_to_select=["route_id","service_id","trip_id","trip_headsign"])
    Trips=Trips.merge(Routes,key="route_id")

    Calendar = calendar(date = date)
    print(Calendar.dateint)
    Calendar = Calendar.select_online_services().Data_Frame

    Calendar_date = calendar_dates(date = date)
    Calendar_date = Calendar_date.select_online_services()
    Calendar_date = Calendar_date.clean(Columns_to_select=["service_id"]).Data_Frame

    Calendar = gtfs(df = pandas.concat([Calendar,Calendar_date]))


    Online_Trips=Trips.merge(Calendar,key="service_id")
    Online_Trips=Online_Trips.clean(Columns_to_select=["agency_name","route_short_name","trip_id","start_date","end_date","route_id","trip_headsign"])

    Stop_times=stop_times()
    Stop_times=Stop_times.merge(Online_Trips,key="trip_id")
    Stop_times=Stop_times.clean(Columns_to_select=["agency_name","route_short_name","trip_id","start_date","end_date","arrival_time","departure_time","stop_id","stop_sequence","route_id","trip_headsign"])

    return Stop_times

def get_link_gtfs_idfm(stop_times):
    """from a stop_times gtfs dataframe containing columns ["agency_name","route_short_name","trip_id","start_date","end_date","arrival_time","departure_time","stop_id","stop_sequence","route_id","trip_headsign"],
    returns a stop gtfs dataframe containing columns ["stop_id",'object_code',"stop_name","stop_lon","stop_lat"]"""
    Stops=stops()
    Stops=Stops.merge(stop_times,key="stop_id")
    Stops=Stops.drop_duplicates("stop_id")
    Stop_extensions=stop_extensions()
    Stop_extensions = Stop_extensions.merge_with_stop(Stops)
    Stop_extensions = Stop_extensions.clean(Columns_to_select=["stop_id",'object_code',"stop_name","stop_lon","stop_lat"])
    """Reflex=reflex()
    Reflex=Reflex.merge_with_stop_extensions(Stop_extensions)
    Reflex=Reflex.clean(Columns_to_select=["stop_id",'ZDEr_ID_REF_A','ZDLr_ID_REF_A','LDA_ID_REF_A','GDL_ID_REF_A',"stop_name","stop_lon","stop_lat"])
    print(Reflex.Data_Frame[Reflex.Data_Frame["stop_id"].map(lambda c:c=="StopPoint:8743088:800:P")],"RECHERCHE P")"""
    Stop_extensions=Stop_extensions.drop_duplicates("stop_id")
    return Stop_extensions

def color_table(Routes):
    """ from Routes gtfs dataframe containing columns ["agency_name","route_short_name","route_color","route_text_color","route_id"] returns a color gtfs dataframe containing ["agency_name","route_short_name","route_id"]"""
    Color=Routes.clean(["agency_name","route_short_name","route_color","route_text_color","route_id"])
    Color=Color.drop_duplicates(["agency_name","route_short_name","route_id"])
    return Color




if __name__ == '__main__':
    DATE=datetime.datetime.now()
    print("configuration DATA")

    RAIL_AGENCIES=["RER","TRAIN","TRAM","TRAMWAY","METRO","Navette"]
    SELECTED_ROUTES = get_routes_of_an_agency(line_agencies=RAIL_AGENCIES)
    MISSIONS = get_trips_data(Routes=SELECTED_ROUTES,date=DATE)
    LINK_GTFS_IDFM = get_link_gtfs_idfm(stop_times=MISSIONS)
    COLOR = color_table(Routes=SELECTED_ROUTES)

    print("DATA configuree")
    print("Exporting data")
    LINK_GTFS_IDFM.Data_Frame.to_excel('datas/LINK_GTFS_IDFM.xlsx')
    MISSIONS.Data_Frame.to_excel('datas/GTFS_MISSIONS.xlsx')
    print("data exported in excel format datas/")
