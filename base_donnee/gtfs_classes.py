import pandas
import datetime
import numpy as np
import networkx as nx
import io
import zipfile
import requests
import os, inspect



GTFS_URL_old = "https://data.iledefrance-mobilites.fr/api/datasets/1.0/offre-horaires-tc-gtfs-idf/images/736ca2f956a1b6cc102649ed6fd56d45"

GTFS_URL = "https://data.iledefrance-mobilites.fr/api/v2/catalog/datasets/offre-horaires-tc-gtfs-idf/files/736ca2f956a1b6cc102649ed6fd56d45"
##### Rappel langue du gtfs
#cf doc RATP : il est super

def download_url(zip_file_url,path):
    print("Downloading files")
    r = requests.get(zip_file_url, stream=True)
    if r.ok:
        print("Download finished succesfully")
        print("unzipping files in", path)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path)
        print("Download process finished")
        return True
    print("an unexpected error occured, please check the doxnloading url")
    return False


class gtfs:
    def __init__(self,df=None,adress=None,low_memory=True,separator=','):
        if adress==None and type(df)!=type(None):
            #appel du constructeur a partir de df
            self.Data_Frame=df
        elif adress!=None and type(df)==type(None):
            #appel constructeur a partir fichier
            self.Data_Frame=pandas.read_csv(adress,low_memory=low_memory,sep=separator)
        else :
            raise AttributeError("Erreur constructeur, il faut préciser en argument soit df (un data frame pandas) soit adress (l'adress d'un fichier csv) mais pas les deux ni aucun")

    def select_lines(self, column , criterion_values ):
        """select lines from self.Data_Frame where column in criterion_values"""
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
        return gtfs(df=(self.Data_Frame.sort_values(by=column)))

    def clean(self,Columns_to_select):
        return self.select_columns(Columns_to_select)



#Variables globales

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
FOLDERS=currentdir+"/datas/IDFM_gtfs/"
REFLEX=currentdir+"/datas/Reflex/REFLEX.csv"
TRACE_FER=currentdir+"/datas/Trace/traces-du-reseau-ferre-idf.csv"
TRACE_BUS=currentdir+"/datas/Trace/bus_lignes.csv"
REF_LIG=currentdir+"/datas/Trace/referentiel-des-lignes.csv"


ADRESS={"agency":FOLDERS+"agency.txt",
"calendar_dates":FOLDERS+"calendar_dates.txt",
"calendar":FOLDERS+"calendar.txt",
"routes":FOLDERS+"routes.txt",
"stop_extensions":FOLDERS+"stop_extensions.txt",
"stop_times":FOLDERS+"stop_times.txt",
"stops":FOLDERS+"stops.txt",
"transfers":FOLDERS+"transfers.txt",
"trips":FOLDERS+"trips.txt",
"reflex":REFLEX,
"trace_fer":TRACE_FER,
"trace_bus":TRACE_BUS,
"ref_lig":REF_LIG }


def import_gtfs(ADRESS):
    DATA={"agency":gtfs(adress=ADRESS["agency"]),
    "calendar_dates":gtfs(adress=ADRESS["calendar_dates"]),
    "calendar":gtfs(adress=ADRESS["calendar"]),
    "routes":gtfs(adress=ADRESS["routes"]),
    "stop_extensions":gtfs(adress=ADRESS["stop_extensions"]),
    "stop_times":gtfs(adress=ADRESS["stop_times"]),
    "stops":gtfs(adress=ADRESS["stops"]),
    "transfers":gtfs(adress=ADRESS["transfers"]),
    "trips":gtfs(adress=ADRESS["trips"],low_memory=False),
    "reflex":gtfs(adress=ADRESS["reflex"],separator="|"),
    "trace_fer":gtfs(adress=ADRESS["trace_fer"],separator=";"),
    "trace_bus":gtfs(adress=ADRESS["trace_bus"],separator=";"),
    "ref_lig":gtfs(adress=ADRESS["ref_lig"],separator=";")
    }
    return DATA


print("Importing gtfs datas")
try :
    DATA = import_gtfs(ADRESS)
except FileNotFoundError :
    print("gtfs files not found, do you want to download it ? y/n")
    if input()=="y" :
        bool = download_url(GTFS_URL,FOLDERS)
        if bool :
            DATA = import_gtfs(ADRESS)
        else :
            raise FileNotFoundError

print("import done")





class stop_times(gtfs):
    def __init__(self,copy=DATA["stop_times"]):
        super().__init__(df=copy.Data_Frame)

    def get_trip(self,trip_id):
        return self.select_lines(column="trip_id",criterion_values=[trip_id]).sort(column="stop_sequence")

class agency(gtfs):
    def __init__(self,copy=DATA["agency"]):
        super().__init__(df=copy.Data_Frame)

class routes(gtfs):
    def __init__(self,copy=DATA["routes"]):
        super().__init__(df=copy.Data_Frame)

    def select_route_on_name(self,route_short_name):
        """selecting a route on name : WARNING possible ambiguity if multiple routes share same short name"""
        if type(route_short_name)==type([]):
            return self.select_lines(column="route_short_name",criterion_values=route_short_name)
        else:
            return self.select_lines(column="route_short_name",criterion_values=[route_short_name])

class trips(gtfs):
    def __init__(self,copy=DATA["trips"]):
        super().__init__(df=copy.Data_Frame)

class stops(gtfs):
    def __init__(self,copy=DATA["stops"]):
        super().__init__(df=copy.Data_Frame)

class stop_extensions(gtfs):
    def __init__(self,copy=DATA["stop_extensions"]):
        super().__init__(df=copy.Data_Frame)

    def merge_with_stop(self,stops):
        a=self.merge_double_key(stops,"object_id","stop_id")
        a=a.select_lines("object_system",["ZDEr_ID_REF_A","source"])
        return a

class reflex(gtfs):
    def __init__(self,copy=DATA["reflex"]):
        super().__init__(df=copy.Data_Frame)
    def merge_with_stop_extensions(self,stop_extensions):
        a=self.merge_double_key(stop_extensions,'ZDEr_ID_REF_A','object_code')
        return a

class transfers(gtfs):
    def __init__(self,copy=DATA["transfers"]):
        super().__init__(df=copy.Data_Frame)

class calendar(gtfs):
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
    def __init__(self,copy=DATA["calendar_dates"]):
        super().__init__(df=copy.Data_Frame)

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

def deal_with_multi_line(MultiLine,extcode):
    """Traite les 3 segments qui sont en MultiLineString au lieu d'etre en LineString """
    ExtCode={"LIGNE P":"800:P","T2":"100112012:T2","T6":"100112016:T6"}
    print("multiLineString detected")
    Line=[]
    MultiLine=MultiLine.to_list()
    if extcode==ExtCode["LIGNE P"]:
        for line in MultiLine:
            Line+=line
        return Line
    if extcode==ExtCode["T6"]:
        for line in MultiLine:
            Line+=line[::-1]
        return Line[::-1]
    if extcode==ExtCode["T2"]:
        s=0
        for line in MultiLine:
            Line+=line[::-1]*(s==0)+line*(s==1)
            s+=1
        return Line[::-1]

def convert_to_single_lineSting(GeoShap,extcode):
    type=GeoShap["type"]
    if type[0]=="MultiLineString":
        return deal_with_multi_line(GeoShap["coordinates"],extcode)
    else:
        return GeoShap["coordinates"].to_list()



class trace_fer(gtfs):
    def __init__(self,copy=DATA["trace_fer"]):
        super().__init__(df=copy.Data_Frame)


    def group_by_line(self):
        self.Data_Frame=self.Data_Frame[["Geo Shape","SHAPE_Leng","id_fmt_tem","OBJECTID","extcode"]]
        self.Data_Frame['Geo Shape']=self.Data_Frame['Geo Shape'].map(lambda c:pandas.read_json(c))
        self.Data_Frame['Geo Shape']=self.Data_Frame.apply(lambda c:convert_to_single_lineSting(c['Geo Shape'],c["extcode"]),axis=1)
        return self.Data_Frame.groupby("extcode")

    def builds_graph_of_single_line(self,grp_route):
        if grp_route.empty:
            raise KeyError("empty dataframe after research on route_id")
        G = nx.Graph()
        for i in grp_route.index :
            V1 = tuple(grp_route["Geo Shape"][i][0])
            V2 = tuple(grp_route["Geo Shape"][i][-1])
            bool1,v1=is_vertice_in_list_based_on_coords_with_epsilon(V1,G.nodes)
            bool2,v2=is_vertice_in_list_based_on_coords_with_epsilon(V2,G.nodes)
            G.add_edge( v1 , v2 , weight = grp_route["SHAPE_Leng"][i] , index = i )
        return G

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
    def __init__(self,copy=DATA["ref_lig"]):
        super().__init__(df=copy.Data_Frame)

class trace_bus(gtfs):
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
    Agency=agency()
    Agency=Agency.clean(Columns_to_select=["agency_id","agency_name"])
    if line_agencies[0]!="ALL" :
        Agency=Agency.select_lines(column="agency_name",criterion_values=line_agencies)

    Routes=routes()
    Routes=Routes.clean(Columns_to_select=["agency_id","route_short_name","route_id","route_color","route_text_color"])
    Routes=Routes.merge(Agency,key="agency_id")
    return Routes


def get_trips_data(Routes,date):
    Trips=trips()
    Trips=Trips.clean(Columns_to_select=["route_id","service_id","trip_id","trip_headsign"])
    Trips=Trips.merge(Routes,key="route_id")

    Calendar=calendar(date=date)

    Calendar=Calendar.select_online_services()

    Online_Trips=Trips.merge(Calendar,key="service_id")
    Online_Trips=Online_Trips.clean(Columns_to_select=["agency_name","route_short_name","trip_id","start_date","end_date","route_id","trip_headsign"])

    Stop_times=stop_times()
    Stop_times=Stop_times.merge(Online_Trips,key="trip_id")
    Stop_times=Stop_times.clean(Columns_to_select=["agency_name","route_short_name","trip_id","start_date","end_date","arrival_time","departure_time","stop_id","stop_sequence","route_id","trip_headsign"])

    return Stop_times

def get_link_gtfs_idfm(stop_times):
    Stops=stops()
    Stops=Stops.merge(stop_times,key="stop_id")
    Stops=Stops.drop_duplicates("stop_id")
    #print(Stops.Data_Frame[Stops.Data_Frame["stop_id"].map(lambda c:c=="StopPoint:8770432:800:T4")],"RECHERCHE T4 1")

    Stop_extensions=stop_extensions()
    #print(Stop_extensions.Data_Frame[Stop_extensions.Data_Frame["object_id"].map(lambda c:c=="StopPoint:8770432:800:T4")],"RECHERCHE T4 2")
    Stop_extensions=Stop_extensions.merge_with_stop(Stops)
    #print(Stop_extensions.Data_Frame[Stop_extensions.Data_Frame["stop_id"].map(lambda c:c=="StopPoint:8770432:800:T4")],"RECHERCHE T4 3")
    Stop_extensions=Stop_extensions.clean(Columns_to_select=["stop_id",'object_code',"stop_name","stop_lon","stop_lat"])
    """Reflex=reflex()
    Reflex=Reflex.merge_with_stop_extensions(Stop_extensions)
    Reflex=Reflex.clean(Columns_to_select=["stop_id",'ZDEr_ID_REF_A','ZDLr_ID_REF_A','LDA_ID_REF_A','GDL_ID_REF_A',"stop_name","stop_lon","stop_lat"])
    print(Reflex.Data_Frame[Reflex.Data_Frame["stop_id"].map(lambda c:c=="StopPoint:8743088:800:P")],"RECHERCHE P")"""
    Stop_extensions=Stop_extensions.drop_duplicates("stop_id")
    return Stop_extensions

def color_table(Routes):
    Color=Routes.clean(["agency_name","route_short_name","route_color","route_text_color","route_id"])
    Color=Color.drop_duplicates(["agency_name","route_short_name","route_id"])
    return Color




if __name__ == '__main__':
    DATE=datetime.datetime.now()
    print("configuration DATA")

    RAIL_AGENCIES=["RER","TRAIN","TRAM","TRAMWAY","METRO","Navette"]
    SELECTED_ROUTES=get_routes_of_an_agency(line_agencies=RAIL_AGENCIES)
    MISSIONS=get_trips_data(Routes=SELECTED_ROUTES,date=DATE)
    LINK_GTFS_IDFM=get_link_gtfs_idfm(stop_times=MISSIONS)
    COLOR=color_table(Routes=SELECTED_ROUTES)

    print("DATA configuree")
    print("Exporting data")
    LINK_GTFS_IDFM.Data_Frame.to_excel('datas/LINK_GTFS_IDFM.xlsx')
    MISSIONS.Data_Frame.to_excel('datas/GTFS_MISSIONS.xlsx')
    print("data exported in excel format datas/")
