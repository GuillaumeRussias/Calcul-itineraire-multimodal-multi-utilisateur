import folium

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
    r=50
    w=5
    for i in range(len(path)-1):
        index,indexp = path[i],path[i+1]
        edge = G[index][indexp][0]
        Station_start = {"folium_coords":(PandaV["stop_lat"][index] , PandaV["stop_lon"][index] ),"name" : PandaV["station_name"][index]}
        Station_end = {"folium_coords":(PandaV["stop_lat"][indexp] , PandaV["stop_lon"][indexp] ),"name" : PandaV["station_name"][indexp]}
        try :
            line_id = edge["route_id"]
        except :
            print("pathwalk")
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
            print("no beatiful display available for that section :( )")
            #pas d'afficahe specifie
            List_diplayable_edges=[Station_start["folium_coords"],Station_end["folium_coords"]]
        else :
            for i in List_diplayable_edges_index:
                folium.PolyLine(idfm_to_folium_coords(PandaDisp_edges["2D_line"][i]),color=color,weight=w,popup=edge_popup,opacity=1).add_to(folium_map)
            #Station_start["folium_coords"] = nearest(Station_start["folium_coords"],Displayable_edge[0],Displayable_edge[-1])
            #Station_end["folium_coords"] = nearest(Station_end["folium_coords"],Displayable_edge[0],Displayable_edge[-1])


        #plot :
        #folium.PolyLine(Displayable_edge,color=color,weight=w,popup=edge_popup,opacity=1).add_to(folium_map)

        folium.Circle(radius=r,location=Station_start["folium_coords"],popup=Station_start["name"],color=color,fill_color=color,fill_opacity=0.8,fill=True).add_to(folium_map)
        folium.Circle(radius=r-40,location=Station_start["folium_coords"],popup=Station_start["name"],color="WHITE",fill_color="WHITE",fill_opacity=0.9,fill=True).add_to(folium_map)

        folium.Circle(radius=r,location=Station_end["folium_coords"],popup=Station_end["name"],color=color,fill_color=color,fill_opacity=0.8,fill=True).add_to(folium_map)
        folium.Circle(radius=r-40,location=Station_end["folium_coords"],popup=Station_end["name"],color="WHITE",fill_color="WHITE",fill_opacity=0.9,fill=True).add_to(folium_map)
    return folium_map
