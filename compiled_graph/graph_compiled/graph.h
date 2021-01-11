// cppimport
#undef NDEBUG

//linker
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
namespace py = pybind11;
//string
#include <iostream>
#include <cassert>
#define assertm(exp, msg) assert(((void)msg, exp))
//vecteur et algorithme de tri
#include <algorithm>
#include <vector>
#include <queue>
#include <array>
#include <deque>
//maths :
#include <limits>


using namespace std;


const int day = 3600*24; //nombre de secondes en 1 jour
const int inf = numeric_limits<int>::max();

inline int convert_seconds(const array<char,8> * hhmmss) {//convert array<char,8> = ["0","8",":","5","0",":","0","0"] into an integer equals of equivalent time in seconds 31800
    return 3600 * (10*(int)(*(hhmmss->begin()) - '0') + (int)(*(hhmmss->begin()+1) - '0')) + 60 * (10*(int)(*(hhmmss->begin()+3) - '0') + (int)(*(hhmmss->begin()+4) - '0')) +  (10*(int)(*(hhmmss->begin()+6) - '0') + (int)(*(hhmmss->begin()+7) - '0'));
}



class edge {
    string type; //"free","scheduled","mixed"-> mandatory to separate transfers(no schedule constraints) from scheduled transportation (scheduled)
    vector<int> id; //id : index of appearance of the mission dep,arr in  build_edges functions (same lenght as departure_time and arrival_time)
    vector<int> departure_time; //" departure times . empty if type=="free" . time in seconds
    vector<int> arrival_time; //" arrival times . empty if type=="free" . time in seconds
    vector<int> trip_id; //"trip id (set to -2 iff undef , -1 iff free)
    int free_cost; // cost in second of the free transfers (equals to 100*day for a sheduled edge)
    int transfers_cost; // cost in seconds of the transfers (define after cost() or cost(t))
    int selected_mission;  //selected mission (define after cost() or cost(t)) = -1 if mission is not sheduled , index of the departure_time arrival_time selected either
    int selected_trip_id;  // selected trip_id  (set to -2 iff undef , -1 iff free)

    void mission(int time);//compute the appropriate mission i of this edge (min time_arrival[i]) s.t (time < time departure[i])
    void mission(int time, int trip_id_prec); //compute the appropriate mission (minimise time+changement)

public :
    edge(int t_departure, int t_arrival, int index , int trip); //scheduled constructor
    edge(int cost); //free constructor


    void push_time(int t_departure, int t_arrival, int index , int trip); //push t_departure, t_arrival
    void set_free_cost(int cost);// set free_cost = cost
    void push_id(int index); // push index in id and check if len(id)==len(departure_time)==len(arrival_time) after

    int cost(); //time independent : totaly ignore edges of type scheduled , works with distance graph
    int cost(int time); //time dependent : works with both gtfs,old graph but takes more time to compute.
    int cost(int time, int trip_id_prec); //time and trip_id dependent.

    int changement_cost(int trip_id_prec); // returns 1 iff selected_trip_id != trip_id_prec and returns 0 either


    string get_type(); //returns type
    pair<int,int> get_selected_mission(); //returns departure_time,arrival_time of selected traject . Intresting after path_finder rerurns -1,cost if free edge selected
    int get_selected_trip_id();//returns the selected trip_id
    int get_transfers_cost(); //returns cost of the transfers. Intresting after path_finder
    int get_id(); //returns id of selected traject . Interesting after path finder returns -1 if free edge selected

    void print_missions();

    };


class vertex {
    int i; //index of the vertex = key
    vector<vertex*> neighbours; //list of neighbours
    vector<edge*> edges; //list of spec of the edge  between this vertex and its neighbours : neighbours[i] <-> edges[i]
public :
    // Dijkstra usefull items
    int time;
    int nb_changements;
    int visited_by_trip_id;
    bool visited;
    vertex* predecessor;

    vertex(int index); // constructor
    void push_neihghbour(vertex* neighbour); // add a neighbour
    void push_edge(edge* edge);// add an edge

    edge* operator[](int j);//safe access to the edge (if it exists) between this and j !return_value_policy::reference! we want c++ to be in charge of the destruction of this object

    //user interface
    vector<int> get_neighbours();
    int get_time();
    bool get_visited();
    int get_predecessor();

    //inline
    inline int get_index(){return i;}
    inline vertex* get_neighbour(int j){return neighbours[j];}
    inline unsigned number_neighbour(){return neighbours.size();}

    inline int cost_of_travel(int j) {return edges[j]->cost();}//returns the cost of the edge between this vertex and the its jth neighbour. time independent
    inline int cost_of_travel(int j, int time) {return edges[j]->cost(time);}//returns the cost of the edge between this vertex and the its jth neighbour. time dependent
    inline int cost_of_travel(int j, int time, int trip_id_prec) { return edges[j]->cost(time, trip_id_prec);}//returns the cost of the edge between this vertex and the its jth neighbour. time and changement dependent
    inline pair<int,int> travel_changement(int j, int trip_id_prec) { return pair<int,int>(edges[j]->changement_cost(trip_id_prec),edges[j]->get_selected_trip_id());} // returns 1 iff selected_trip_id != trip_id_prec and returns 0 either
};


class graph {
    vector<vertex*> v_list; //list of vertices
    vector<edge*> e_list; //list of edges
    void push_free_edge(int departure_index, int arrival_index, int cost); //push a single free edge
    void push_scheduled_edge(int departure_index, int arrival_index, int departure_time, int arrival_time, int id); //push a single scheduled edge
    void push_scheduled_edge(int departure_index, int arrival_index, int departure_time, int arrival_time, int id , int trip); //push a single scheduled edge with trip_id
    void push_vertex(int index); //push a vertex
public :
    //tools functions
    graph(int size_v); //constructor
    ~graph();//destructor
    void build_scheduled_edges(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<int> departure_time, py::array_t<int> arrival_time , py::array_t<int> edge_id); //construct all scheduled edges
    void build_free_edges(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<int> cost); //construct all free edges

    void build_scheduled_edges_string(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<array<char,8>> departure_time, py::array_t<array<char,8>> arrival_time, py::array_t<int> edge_id); //construct all scheduled edges
    void build_scheduled_edges_string_trip_id(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<array<char, 8>> departure_time, py::array_t<array<char, 8>> arrival_time, py::array_t<int> edge_id, py::array_t<int> trip_id); //construct all scheduled edges with trip_id

    vertex* operator[](int i); //safe access to the ith vertex of the graph !return_value_policy::reference! we want c++ to be in charge of the destruction of this object
    void initialised(); //set all (visited,time) at (false,inf)


    //algorithms : carefull : graph needs to be re-initialised (visited, time) after the execution of these 4 algorithms
    void basic_djikstra(int start_vertex_index); //basic djikstra
    int multi_users_dijkstra(py::array_t<int> start_indexes,int t); //Dijkstra plusieurs utilisateurs, renvoie le somme d'arrivée optimal
    void time_djikstra(int start_vertex_index, int t); //time dependant djikstra
    void stop_basic_djikstra(int start_vertex_index, int end_vertex_index); //basic djikstra , with stop condition
    void stop_time_djikstra(int start_vertex_index, int end_vertex_index, int t); //time dependant djikstra , with stop condition

    void time_changements_djikstra(int start_vertex_index, int t);
    void stop_time_changements_djikstra(int start_vertex_index, int end_vertex_index, int t);

    //user interface
    vector<int> path_finder(int start_vertex_index, int end_vertex_index); //With stop condition returns path from start to end (index of vertex) trow exception if no path is find , graph re-initialised after execution
    vector<int> path_finder_time(int start_vertex_index, int end_vertex_index, int t); //With stop condition + TIME . returns path from start to end (index of vertex) trow exception if no path is find , graph re-initialised after execution
    vector<int> complete_path_finder(int start_vertex_index, int end_vertex_index); //path_finder but with a complete basic djikstra
    vector<int> complete_path_finder_time(int start_vertex_index, int end_vertex_index, int t); //time_path_finder but with a complete time djikstra

    vector<int> complete_path_finder_time_changement(int start_vertex_index, int end_vertex_index, int t);
    vector<int> path_finder_time_changement(int start_vertex_index, int end_vertex_index, int t);

};

class comparetime {
public:
     inline bool operator()( vertex* A, vertex* B ) {
        return (A->time > B->time);
    }
};

class comparetime_and_changements{
public:
    inline bool operator()(vertex* A, vertex* B) {
        return (A->time > B->time) || (!(A->time < B->time) && (A->nb_changements > B->nb_changements));
        //return (A->nb_changements > B->nb_changements) || (!(A->nb_changements < B->nb_changements) && (A->time > B->time));
    }
};
