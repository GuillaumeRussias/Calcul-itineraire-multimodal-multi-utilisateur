// cppimport

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
#include <deque>

using namespace std;

const int day = 3600*24; //nombre de secondes en 1 jour

class myClass
{
public:
    int number;

    myClass();
    void addOne();

    int getNumber();
};

class edge {
    string type; //"free","scheduled","mixed"-> mandatory to separate transfers(no schedule constraints) from scheduled transportation (scheduled)
    vector<int> departure_time; //" departure times . empty if type=="free" . time in seconds
    vector<int> arrival_time; //" arrival times . empty if type=="free" . time in seconds
    int free_cost; // cost in second of the free transfers (equals to 100*day for a sheduled edge)
    int transfers_cost; // cost in seconds of the transfers (define after cost() or cost(t))
    int selected_mission;  //selected mission (define after cost() or cost(t)) = -1 if mission is not sheduled , index of the departure_time arrival_time selected either
    void mission(int time);//compute the appropriate mission i of this edge (min time_arrival[i]) s.t (time < time departure[i]), throw exception if called for a free edge
public :
    int id; //id of the edge (index of its first appearance in build_edges functions)
    edge(int departure_t, int arrival_t); //scheduled constructor
    edge(int cost); //free constructor

    void push_time(int t_departure, int t_arrival); //push t_departure, t_arrival
    void set_free_cost(int cost);// set free_cost = cost

    int cost(); //time independent : totaly ignore edges of type scheduled , works with distance graph
    int cost(int time); //time dependent : works with both gtfs,old graph but takes more time to compute.

    string get_type(); //returns type
    pair<int,int> get_selected_mission(); //returns departure_time,arrival_time of selected traject . Intresting after path_finder
    int get_transfers_cost(); //returns cost of the transfers. Intresting after path_finder
    int get_id(); //returns id

    };


class vertex {
    int i; //index of the vertex = key
    vector<vertex*> neighbours; //list of neighbours
    vector<edge*> edges; //list of spec of the edge  between this vertex and its neighbours : neighbours[i] <-> edges[i]
public :
    // Dijkstra usefull items
    int time;
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
};


class graph {
    vector<vertex*> v_list; //list of vertices
    vector<edge*> e_list; //list of edges
    void push_free_edge(int departure_index, int arrival_index, int cost, int id); //push a single free edge
    void push_scheduled_edge(int departure_index, int arrival_index, int departure_time, int arrival_time, int id); //push a single scheduled edge
    void push_vertex(int index); //push a vertex
public :
    //tools functions
    graph(int size_v); //constructor
    ~graph();//destructor
    void build_scheduled_edges(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<int> departure_time, py::array_t<int> arrival_time , py::array_t<int> edge_id); //construct all scheduled edges
    void build_free_edges(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<int> cost, py::array_t<int> edge_id); //construct all free edges
    vertex* operator[](int i); //safe access to the ith vertex of the graph !return_value_policy::reference! we want c++ to be in charge of the destruction of this object
    void initialised(); //set all (visited,time) at (false,7*day)

    //algorithms : carefull : graph needs to be re-initialised (visited, time) after the execution of these 4 algorithms
    void basic_djikstra(int start_vertex_index); //basic djikstra
    void time_djikstra(int start_vertex_index, int t); //time dependant djikstra
    void stop_basic_djikstra(int start_vertex_index, int end_vertex_index); //basic djikstra , with stop condition
    void stop_time_djikstra(int start_vertex_index, int end_vertex_index, int t); //time dependant djikstra , with stop condition

    //user interface
    vector<int> path_finder(int start_vertex_index, int end_vertex_index); //returns path from start to end (index of vertex) trow exception if no path is find , graph re-initialised after execution
    vector<int> path_finder_time(int start_vertex_index, int end_vertex_index, int t); //TIME . returns path from start to end (index of vertex) trow exception if no path is find , graph re-initialised after execution

};

class comparetime {
public:
     inline bool operator()( vertex* A, vertex* B ) {
        return (A->time > B->time);
    }
};
