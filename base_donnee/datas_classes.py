import json
import copy
from base_donnee import tree
from base_donnee import tools

#import tree
#import tools

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


class lignes_gtfs(IDFM):
    def __init__(self,file_adress):
        super().__init__(file_adress)

    def get_important_data(self):
        coords=self.get_values_of_keys("coordinates") #multiple_array_dim :coords[ligne[1][missions[coordonnees_stops]]]
        line_names=self.get_values_of_keys("route_short_name")
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
        #on garde les plus grandes missions au sens de l'inclusion
        #tres utile, ex: pour le RER D le nombre de mission passe de 136 a 6 !
        lignes_gtfs.coords_treatment(coords)

        return coords,line_names,line_colors,line_types

class referenciel_lignes(IDFM):
    def __init__(self,file_adress):
        super().__init__(file_adress)
    def get_color_and_name(self):
        #self.get_keys_short(6)
        """retourne un dictionnaire liant nom de ligne et couleur """
        line_names=self.get_values_of_keys("shortname_line")
        line_colors=self.get_values_of_keys("colourweb_hexa")
        line_types=self.get_values_of_keys("transportmode")
        s=0
        for i in range(len(line_types)):
            if line_types[i][1] in ["Bus","bus"] :
                del line_names[i-s]
                del line_colors[i-s]
                s+=1
        assert(len(line_names)==len(line_colors)),"Important error in lignes_gtfs(IDFM) data exploitation"
        dict={}
        def check_nom(nom):
            if nom=="CDG VAL":
                return "CDG"
            if nom=="ORLYVAL":
                return "ORL"
            if nom=="3B":
                return "3b"
            if nom=="7B":
                return "7b"
            return nom
        for i in range(len(line_names)):
            dict[check_nom(line_names[i][1])]=line_colors[i][1]
        return dict



    @staticmethod
    def coords_treatment(coords):
        for i in range(len(coords)):
            #coords[i][1]=ensemble missions sur la ligne. On veut garder les missions les plus grandes  au sens de l'inclusion
            tools.garder_plus_grands_elements_sens_inclusion(coords[i][1])

class trace_lignes_idf(IDFM):
    def __init__(self,file_adress):
        super().__init__(file_adress)
    def get_important_data(self):
        liaisons_developpees=self.get_values_of_keys("coordinates")
        cout_liaison=self.get_values_of_keys("shape_leng")
        ligne_liaison=self.get_values_of_keys("indice_lig")
        type_liason=self.get_values_of_keys("type") #multiline array ou line array
        real_name_of_line=self.get_values_of_keys("res_com")
        s=0
        nom=copy.deepcopy(ligne_liaison)
        for i in range(len(type_liason)):
            if type_liason[i][1] in ["MultiLineString"] or nom[i][1] in ["GL","TER"]:
                del liaisons_developpees[i-s]
                del cout_liaison[i-s]
                del ligne_liaison[i-s]
                del real_name_of_line[i-s]
                s+=1
        for i in range(len(cout_liaison)):
            if real_name_of_line[i][1] in ["T1","T2","T3A","T3B","T4","T5","T6","T7","T8","T9"]:
                ligne_liaison[i][1] = real_name_of_line[i][1]

        assert(len(liaisons_developpees)==len(cout_liaison) and len(cout_liaison)==len(ligne_liaison)),"Important error in trace_lignes_(IDFM) data exploitation"
        return liaisons_developpees,cout_liaison,ligne_liaison



"""
lignes=trace_lignes_idf("datas/traces-du-reseau-ferre-idf.json")
lignes.get_keys_short(111);
lignes.get_important_data()"""
"""keys=["type","metro","rer","indice_lig","shape_leng"]
for key in keys:
    print(key,lignes.get_values_of_keys_short(key))
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
