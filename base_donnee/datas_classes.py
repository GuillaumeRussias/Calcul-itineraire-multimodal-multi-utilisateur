import json
import copy
from base_donnee import tree
from base_donnee import tools




class json_database:
    """mother class to deal with every JSON database"""
    def __init__(self,file_adress):
        self._file=open(file_adress,'r',errors='ignore')
        self._dict=json.load(self._file)
        self.get_keys(file_adress)

    def get_keys(self,name="Tree of Keys for dictionnary"):
        """create a tree structure which contains all the key of json dictionnary"""
        self.tree_keys=tree.Tree(name)
        self.tree_keys.build_from_iterable(self._dict)

    def display_keys(self):
        self.tree_keys.display('*','|---')

    def search_key_and_ancestors(self,key):
        try :
            tuple=self.tree_keys.deep_research(key)
        except ValueError as Verr:
            print("[ValueError] json_database/search_key_and_ancestors(self,key) no key find ",Verr,": returning empty tuple")
            return ()
        else:
            return tuple

    def get_sub_dict_from_dict(self,sub_dict_adress):
        """extract a dict at the adress keys_to_value from self._dict"""
        dict=self._dict
        for i in range(1,len(sub_dict_adress)):
            dict=dict[sub_dict_adress[i]]
        return dict

    def get_values_of_keys(self,key):
        """extract all values linked with a key and put it in a list=[[address,value]]"""
        research_tuple=self.search_key_and_ancestors(key)
        research_list=[i for i in research_tuple]
        adress_and_values=[]
        bool=True
        while bool:
            n=tools.search_last_int_index_iterable(research_list)
            if n==None:
                adress_and_values.append([research_list,self.get_sub_dict_from_dict(research_list)])
                bool=False
            else:
                try :
                    adress_and_values.append([copy.deepcopy(research_list),self.get_sub_dict_from_dict(research_list)])
                except KeyError as kEr:
                    "Warning: this element doesn't has key_value as key"
                except IndexError:
                    "end of list reached"
                    #print("[get_values_of_keys] size of list in dictionnary",research_list[n])
                    bool=False
                finally:
                    research_list[n]+=1
        return adress_and_values

    def get_values_of_keys_short(self,key):
        """"same function as get_values_of_keys just without doublons"""
        adress_and_values=self.get_values_of_keys(key)
        return_list=[]
        for el in adress_and_values:
            if el[1] not in return_list:
                return_list.append(el[1])
        return return_list


class OpenStreetMap(json_database):
    """Class to deal with datas from OpenStreet map  """
    def __init__(self,file_adress):
        super().__init__(file_adress)

    def get_keys_short(self,i):
        """in this specific database, _dict[elements][i] contains most important information, we extract the key of that dict  """
        keys_short=tree.Tree('elements of transport_idf._dict[elements][i] ')
        keys_short.build_from_iterable(self._dict['elements'][i])
        keys_short.display('*','|---')
        return keys_short
    def get_important_data(self):
        lat=self.get_values_of_keys('lat')
        lon=self.get_values_of_keys('lon')
        id=self.get_values_of_keys('id')
        type=self.get_values_of_keys('type')
        s=0
        for i in range(len(type)):
            if type[i][1]!='node':
                del id[i-s]
                s+=1
        assert(len(lat)==len(lon) and len(id)==len(lat)),"Important error in OpenStreetMap(json_database) data exploitation"
        return lat,lon,id


"""
    def List_vertice_creator(self):
        lat=self.get_values_of_keys('lat')
        lon=self.get_values_of_keys('lon')
        id=self.get_values_of_keys('id')
        type=self.get_values_of_keys('type')
        s=0
        for i in range(len(type)):
            if type[i][1]!='node':
                del id[i-s]
                s+=1
        list_vertice=[]
        for i in range(len(lat)):
            coords=np.array([lon[i][1],lat[i][1]])
            iD=id[i][1]
            list_vertice.append(class_vertice_graph.Vertice(i,coords))
            list_vertice[-1].id=iD
        return list_vertice

    @staticmethod
    def find_index_of_vertice_where_id_equals(id,list_vertice):
        for i in range (len(list_vertice)):
            if list_vertice[i].id==id:
                return i
    def get_line_names(self):
        names=self.get_values_of_keys("name")
        print(len(names))

    def way_creator(self,List_Vertice):
        id=self.get_values_of_keys('id')
        type=self.get_values_of_keys('type')
        nodes_id=self.get_values_of_keys('nodes')
        s=0
        for i in range(len(type)):
            if type[i][1]=='node':
                del id[i-s]
                s+=1
        for i in range(len(id)):
            assert (nodes_id[i][0][-2]==id[i][0][-2]),"index error in data base "+str(nodes_id[i][0][-2])+","+str(id[i][0][-2])
            for identity_vertice_index in range(len(nodes_id[i])-1):
                j=identity_vertice_index
                j_next=identity_vertice_index+1
                Vj_index=OpenStreetMap.find_index_of_vertice_where_id_equals(nodes_id[i][1][j],List_Vertice)
                if Vj_index==None:
                    print(j)
                Vj_next_index=OpenStreetMap.find_index_of_vertice_where_id_equals(nodes_id[i][1][j_next],List_Vertice)
                if Vj_next_index==None:
                    print(j_next)
                edje=class_vertice_graph.Edge(List_Vertice[Vj_index],List_Vertice[Vj_next_index],id[i][1])
                List_Vertice[Vj_index].push_edge(edje)

    def graph_creator(self):
        List_Vertice=self.List_vertice_creator()
        self.way_creator(List_Vertice)
        return class_vertice_graph.Graph(List_Vertice)
"""


class IDFM(json_database):
    """Class to deal with datas : referentiel from Ile de France Mobilite  """
    def __init__(self,file_adress):
        super().__init__(file_adress)

    def get_keys_short(self,i):
        """in this specific database, _dict[i] contains most important information, we extract the key of that dict   """
        keys_short=tree.Tree('short_keys')
        keys_short.build_from_iterable(self._dict[i])
        keys_short.display('*','|---')
        return keys_short


class emplacement_gares(IDFM):
    def __init__(self,file_adress):
        super().__init__(file_adress)

    def get_important_data(self):
        coords=self.get_values_of_keys("coordinates")
        id=self.get_values_of_keys("gares_id")
        names=self.get_values_of_keys("nom_gare")
        assert(len(coords)==len(id) and len(id)==len(names)),"Important error in  emplacement_gares(IDFM) data exploitation"
        return coords,id,names

"""
    def  List_vertice_creator(self):
        coords=self.get_values_of_keys("coordinates")
        id=self.get_values_of_keys("gares_id")
        names=self.get_values_of_keys("nom_gare")
        print(len(names),len(id))
        list_vertice=[]
        for index in range(len(id)):
            list_vertice.append(class_vertice_graph.Vertice(index,coords[index][1]))
            list_vertice[-1].id=id[index][1]
            list_vertice[-1].gare_name=names[index][1]
        return list_vertice
"""

class lignes_gtfs(IDFM):
    def __init__(self,file_adress):
        super().__init__(file_adress)

    def get_important_data(self):
        coords=self.get_values_of_keys("coordinates") #multiple_array_dim :coords[ligne[1][missions[coordonnees_stops]]]
        line_names=self.get_values_of_keys("route_long_name")
        line_colors=self.get_values_of_keys("route_color")
        line_types=self.get_values_of_keys("route_type")
        s=0
        list_types=copy.deepcopy(line_types)
        list_name=copy.deepcopy(line_names)
        for i in range(len(list_types)):
            if list_types[i][1] in ["Bus","bus"] or list_name[i][1] in ["TER"] :
                del line_names[i-s]
                del coords[i-s]
                del line_colors[i-s]
                del line_types[i-s]
                s+=1
        assert(len(coords)==len(line_names) and len(line_colors)==len(line_types) and len(coords)==len(line_names)),"Important error in lignes_gtfs(IDFM) data exploitation"
        lignes_gtfs.coords_treatment(coords)
        return coords,line_names,line_colors,line_types

    @staticmethod
    def coords_treatment(coords):
        for i in range(len(coords)):
            #coords[i][1]=ensemble missions sur la ligne. On veut garder les missions les plus grandes  au sens de l'inclusion
            tools.garder_plus_grands_elements_sens_inclusion(coords[i][1])

"""
    def link_vertices(self,list_vertices):
        coords,line_names,line_colors,line_types=self.get_lines()
        int=0
        for key,line in coords:
            for mission in line:
                for j in range(len(mission)):
                    if j<len(mission)-1:
                        stop=mission[j]
                        stopplus=mission[j+1]
                        list_index_j=lignes_gtfs.find_corresponding_vertice_index(list_vertices,stop)
                        list_index_jplus=lignes_gtfs.find_corresponding_vertice_index(list_vertices,stopplus)
                        for jj in list_index_j:
                            for jjp in list_index_jplus:
                                vj=list_vertices[jj]
                                vjp=list_vertices[jjp]
                                id=line_names[int]
                                edge=class_vertice_graph.Edge(vj,vjp,id)
                                if edge not in list_vertices[jj].edges_list:
                                    list_vertices[jj].push_edge(edge)
            int+=1

    @staticmethod
    def find_corresponding_vertice_index(list_vertices,coords):
        index=[]
        for i in range(len(list_vertices)):
            v=list_vertices[i]
            if ((coords[0]-v.coordinates[0])**2)+((coords[1]-v.coordinates[1]))**2<epsilon :
                index.append(i)
        return index
"""















"""
referentiel_lignes=IDFM("datas/referentiel-des-lignes.json")
lignes_gtfs=lignes_gtfs("datas/lignes-gtfs.json")
referentiel_gares=emplacement_gares("datas/Referenciel_gares/emplacement-des-gares-idf.json")
transport_idf= OpenStreetMap("datas/transport_idf_open_streetmap.json")

lignes_gtfs.get_important_data()
"""
"""

#a=referentiel_gares.List_vertice_creator()
#lignes.link_vertices(a)
#c=class_vertice_graph.Graph(a)
#c.plot()


#referentiel_gares.get_keys_short(8)
#a=referentiel_gares.List_vertice_creator()
#b=class_vertice_graph.Graph(a)
#b.plot()
#transport_idf.get_keys_short(7)

#transport_idf.display_keys()
#transport_idf.get_keys_short(7)
#transport_idf.search_key_and_ancestors("lat")
#transport_idf.get_values_of_keys("lat")
#transport_idf.get_values_of_key("lat")
#graph=transport_idf.graph_creator()
#graph.plot()

#referentiel_lignes.get_keys()
#referentiel_lignes.search_key_and_ancestors("line_ID")
#referentiel_lignes.display_keys()
"""
