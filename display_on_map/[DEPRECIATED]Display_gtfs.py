
#DEPRECIATED - not used by final programm


import folium
import numpy as np
import datetime

def idfm_to_folium_coords(list2D):
    for v in list2D:
        v[0],v[1]=v[1],v[0]
    return list2D
def nearest(M,V1,V2):
    d1=(V1[0]-M[0])**2+(V1[1]-M[1])**2
    d2=(V2[0]-M[0])**2+(V2[1]-M[1])**2
    if d1<=d2:
        return V1
    else :
        return V2

def plot_traject_folium(folium_map,path,PandaV,PandaDisp_edges,PandaC,G):
    r=30
    w=5
    for i in range(len(path)-1):
        index,indexp = path[i],path[i+1]
        edge = G[index][indexp][0]
        Station_start = {"folium_coords":(PandaV["stop_lat"][index] , PandaV["stop_lon"][index] ),"name" : PandaV["station_name"][index]}
        Station_end = {"folium_coords":(PandaV["stop_lat"][indexp] , PandaV["stop_lon"][indexp] ),"name" : PandaV["station_name"][indexp]}
        try :
            line_id = edge["route_id"]
        except :
            #typiquement une liaison pedestre n'a pas d'identifiant de ligne
            color = "grey"
            line_name = "laison pedestre, temps de marche : " + str(edge["weight"])
            edge_popup = line_name
        else :
            departure_time = edge["departure_time"]
            arrival_time = edge["arrival_time"]
            SelectedLinePandaC=PandaC[PandaC["route_id"].map(lambda c:c==line_id)].index[0]
            color = "#"+PandaC["route_color"][SelectedLinePandaC]
            line_name = PandaC["route_short_name"][SelectedLinePandaC]
            edge_popup = line_name + " departure: " + departure_time + " arrival: "+arrival_time

        try :
            List_diplayable_edges_index = edge["list_of_disp_edge_index"]
        except :
            #pas d'afficahe specifie
            folium.PolyLine([Station_start["folium_coords"],Station_end["folium_coords"]],color=color,weight=w,popup=edge_popup,opacity=1).add_to(folium_map)
        else :
            for i in List_diplayable_edges_index:
                folium.PolyLine(idfm_to_folium_coords(PandaDisp_edges["2D_line"][i]),color=color,weight=w,popup=edge_popup,opacity=1).add_to(folium_map)
            #Station_start["folium_coords"] = nearest(Station_start["folium_coords"],Displayable_edge[0],Displayable_edge[-1])
            #Station_end["folium_coords"] = nearest(Station_end["folium_coords"],Displayable_edge[0],Displayable_edge[-1])


        #plot :
        #folium.PolyLine(Displayable_edge,color=color,weight=w,popup=edge_popup,opacity=1).add_to(folium_map)

        folium.Circle(radius=r,location=Station_start["folium_coords"],popup=Station_start["name"],color=color,fill_color=color,fill_opacity=0.8,fill=True).add_to(folium_map)
        folium.Circle(radius=r-10,location=Station_start["folium_coords"],popup=Station_start["name"],color="WHITE",fill_color="WHITE",fill_opacity=0.9,fill=True).add_to(folium_map)

        folium.Circle(radius=r,location=Station_end["folium_coords"],popup=Station_end["name"],color=color,fill_color=color,fill_opacity=0.8,fill=True).add_to(folium_map)
        folium.Circle(radius=r-10,location=Station_end["folium_coords"],popup=Station_end["name"],color="WHITE",fill_color="WHITE",fill_opacity=0.9,fill=True).add_to(folium_map)
    return folium_map

def get_best_edge(edges_list,time):
    t_start_day=time.replace(hour=0,minute=0,second=0)
    min=time.replace(year=time.year+1)
    e_min=0
    for e in edges_list.values():
        if e["type"]!="walk":
            t_start = t_start_day + datetime.timedelta(hours=int(e["departure_time"][0:2]),minutes=int(e["departure_time"][3:5]),seconds=int(e["departure_time"][6:8]))
            t_end = t_start_day + datetime.timedelta(hours=int(e["arrival_time"][0:2]),minutes=int(e["arrival_time"][3:5]),seconds=int(e["arrival_time"][6:8]))
            if t_end<=min and t_start>=time:
                min = t_end
                e_min = e
    if min!=time.replace(year=time.year+1):
        return e_min
    else :
        for e in edges_list.values():
            if e["type"]=="walk":
                return e
    print("pb")
    return  edges_list[0]


def nearest_station(v,list):
    vmin = np.inf
    min = np.inf
    for h in list :
        d = (h[0]-v[0])**2 +(h[1]-v[1])**2
        if d<=min :
            vmin = h
            min = d
    return vmin



def plot_traject_folium2(folium_map,path,PandaV,PandaDisp_edges,PandaC,G,PandaDisp_edgesBus,time):
    r=10
    w=4
    for i in range(1,len(path)):
        im = i-1
        edge = get_best_edge(G[path[im]][path[i]],time)
        j = path[i]
        jm = path[im]
        time = time + datetime.timedelta(seconds = int(edge["weight"]))
        if edge["type"]=="walk":
            color= "grey"
            edge_popup = "laison pedestre, temps de marche : " + str(edge["weight"])+ " s"
            index_display = 0
            index_displaybus = None
        else :
            SelectedLinePandaC=PandaC[PandaC["route_id"].map(lambda c:c==edge["route_id"])].index[0]
            color = "#"+PandaC["route_color"][SelectedLinePandaC]
            edge_popup = PandaC["route_short_name"][SelectedLinePandaC] + " departure: " + edge["departure_time"] + " arrival: "+ edge["arrival_time"]
            index_display = edge["list_of_disp_edge_index"]
            index_displaybus = edge["disp_edge_index_bus"]

        if type(index_display)==type([]) : #on trace un chemin de fer
            extrems = []
            for h in index_display :
                troncon = idfm_to_folium_coords(PandaDisp_edges["2D_line"][h])
                folium.PolyLine(troncon,color=color,weight=w,popup=edge_popup,opacity=1).add_to(folium_map)
                extrems.append(troncon[0])
                extrems.append(troncon[-1])
            Station_start = {"folium_coords" : nearest_station((PandaV["stop_lat"][jm] , PandaV["stop_lon"][jm] ),extrems),"name" : PandaV["station_name"][jm]}
            Station_end = {"folium_coords": nearest_station((PandaV["stop_lat"][j] , PandaV["stop_lon"][j] ),extrems),"name" : PandaV["station_name"][j]}

        elif type(index_displaybus)==type(1) : #on trace une ligne de bus
            troncon = idfm_to_folium_coords(PandaDisp_edgesBus[index_displaybus])
            extrems=[troncon[0],troncon[-1]]
            folium.PolyLine(troncon,color=color,weight=w,popup=edge_popup,opacity=1).add_to(folium_map)
            Station_start = {"folium_coords" : nearest_station((PandaV["stop_lat"][jm] , PandaV["stop_lon"][jm] ),extrems),"name" : PandaV["station_name"][jm]}
            Station_end = {"folium_coords": nearest_station((PandaV["stop_lat"][j] , PandaV["stop_lon"][j] ),extrems),"name" : PandaV["station_name"][j]}
            index_displaybus = None
        else :
            Station_start = {"folium_coords" : (PandaV["stop_lat"][jm] , PandaV["stop_lon"][jm] ),"name" : PandaV["station_name"][jm]}
            Station_end = {"folium_coords" : (PandaV["stop_lat"][j] , PandaV["stop_lon"][j] ),"name" : PandaV["station_name"][j]}
            folium.PolyLine([Station_start["folium_coords"],Station_end["folium_coords"]],color=color,weight=w,popup=edge_popup,opacity=1).add_to(folium_map)

        folium.Circle(radius=r,location=Station_start["folium_coords"],popup=Station_start["name"],color=color,fill_color="WHITE",fill_opacity=1,fill=True).add_to(folium_map)
        folium.Circle(radius=r,location=Station_end["folium_coords"],popup=Station_end["name"],color=color,fill_color="WHITE",fill_opacity=1,fill=True).add_to(folium_map)

    print(time)
    return folium_map
