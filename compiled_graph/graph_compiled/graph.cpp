// cppimport

#include "graph.h"


vertex::vertex(int index) {
    time = inf;
    visited = false;
    i = index;
}
void vertex::push_neihghbour(vertex* neighbour) {
    neighbours.push_back(neighbour);
}
void vertex::push_edge(edge* edge) {
    edges.push_back(edge);
}
edge* vertex::operator[](int j){
    for (unsigned k = 0; k < neighbours.size(); k++) {
        if (neighbours[k]->i == j) {
            return edges[k];
        }
    }
    throw invalid_argument("These vertices are not linked");
}


vector<int> vertex::get_neighbours(){
  vector<int> to_return;
    for (int i=0;i<number_neighbour();i++){
      to_return.push_back(neighbours[i]->i);
    }
  return to_return;
}

int vertex::get_time(){
  return time;
}
bool vertex::get_visited(){
  return visited;
}
int vertex::get_predecessor(){
  return predecessor->i;
}


void edge::print_missions(){
  cout<<endl;
  cout<<"================================="<<endl;
  cout<<"type : "<<type<<endl;
  for(int i=0;i<departure_time.size();i++){
    cout<<i<<" departure : "<< departure_time[i] <<" arrival : "<< arrival_time[i] <<" id : "<<id[i]<<endl;
  }
  cout<<"selected mission : " << selected_mission <<endl;
  cout<<"cost : "<< transfers_cost <<endl;
  cout<<"================================="<<endl;
}

edge::edge(int cost) {
    type = "free";
    free_cost = cost;
}

edge::edge(int departure_t, int arrival_t, int index) {
    departure_time.push_back(departure_t);
    arrival_time.push_back(arrival_t);
    push_id(index); //on rajoute l'identifiant
    type = "scheduled";
    free_cost = inf;
}


void edge::set_free_cost(int cost) {
    if (type == "scheduled")type = "mixed";
    free_cost = cost;
}
void edge::push_id(int index){
    id.push_back(index);
    assertm(id.size() == departure_time.size() && id.size() == arrival_time.size(), "id, departure_time, arrival_time must have same lenght");
}
void edge::push_time(int t_departure, int t_arrival, int index) {
    if (type == "free")type = "mixed";
    departure_time.push_back(t_departure);
    arrival_time.push_back(t_arrival);
    push_id(index); //on rajoute l'identifiant
}


int edge::cost() { //cout de la liaison , cas independant du temps
    if (type == "free" || type == "mixed") { // si une liaison libre est definie on retourne sa valeur
        transfers_cost = free_cost;
        selected_mission = -1;
    }
    else { //sinon on "transforme la premiere liason schedulee en liaison libre
        transfers_cost = arrival_time[0] - departure_time[0];
        selected_mission = 0;
    }
    return transfers_cost;
}

int edge::cost(int time){//cout de la liaison , cas dependant du temps
    if (type == "scheduled" || type == "mixed") mission(time); // on cherche la liason minimisant t_arrivee sous contrainte t_depard>=t
    else {//dans le cas d'une liasion libre la question ne se pose pas
        selected_mission = -1;
        transfers_cost = free_cost;
    }
    return transfers_cost;
}

void edge::mission(int time){
    int cost;
    int min = free_cost;
    int i_min = -1;
    for (unsigned i = 0; i < departure_time.size(); i++) {
        if (departure_time[i] < time) cost = arrival_time[i] - time + day;
        else cost = arrival_time[i] - time;
        if (cost <= min) {
            min = cost;
            i_min = int(i);
        }
    }
    transfers_cost = min;
    selected_mission = i_min;
    assertm(transfers_cost>=0,"no negative cost allowed");
}

string edge::get_type(){
  return type;
}
pair<int,int> edge::get_selected_mission(){
  if (selected_mission!=-1){
    return pair<int,int>(departure_time[selected_mission],arrival_time[selected_mission]);
  }
  else return pair<int,int>(-1,free_cost);
}
int edge::get_transfers_cost(){
  return transfers_cost;
}

int edge::get_id(){
    if (selected_mission == -1) return selected_mission;
    return id.at(selected_mission);
}

graph::graph(int size_v) {
    if (size_v > 0) {
        v_list = vector<vertex*>(size_v);
        for (int i = 0; i < size_v; i++) {
            v_list[i] = new vertex(i);
        }
    }
    else {
        cerr << "No correct size given in graph constructor, creating empty graph . Compute time is longer .";
    }
}
graph::~graph() {
    cout << "appel detructeur" << endl;
    for (unsigned i = 0; i < v_list.size(); i++) {
        delete v_list[i];
    }
    for (unsigned i = 0; i < e_list.size(); i++) {
        delete e_list[i];
    }
}


void graph::push_vertex(int index) {
    int last = v_list.size() - 1;
    while (index > last) {
        last++;
        v_list.push_back(new vertex(last));
    }
}

void graph::push_scheduled_edge(int departure_index, int arrival_index, int departure_time, int arrival_time, int id) {
    assertm(arrival_time>=departure_time, "negative cost not allowed");
    try {
        this->operator[](departure_index)->operator[](arrival_index)->push_time(departure_time, arrival_time, id); //on ajoute les horaires departs et arrivee si l'edge est deja definie et l'identifiant
    }
    catch (invalid_argument) { //sinon on cree une nouvelle edge
        push_vertex(departure_index);//si le sommet n'est pas deja defini, alors on le defini. si il est deja defini cette fonction ne fait rien
        push_vertex(arrival_index);
        if (departure_index >= int(v_list.size()) || departure_index < 0 || arrival_index >= int(v_list.size()) || arrival_index < 0) throw out_of_range("can't push an edge with vertices not in the graph");//petit test
        e_list.push_back(new edge(departure_time, arrival_time, id));
        v_list[departure_index]->push_neihghbour(v_list[arrival_index]);
        v_list[departure_index]->push_edge(e_list.back());
    }
}

void graph::push_free_edge(int departure_index, int arrival_index, int cost) {
    assertm(cost>=0, "negative cost not allowed");
    try {
        this->operator[](departure_index)->operator[](arrival_index)->set_free_cost(cost); //on ajoute la liaison libre si l'edge est deja definie
    }
    catch (invalid_argument) { //sinon on cree une nouvelle edge
        push_vertex(departure_index); //si le sommet n'est pas deja defini, alors on le defini. siil est deja defini cette fonction ne fait rien
        push_vertex(arrival_index);
        if (departure_index >= int(v_list.size()) || departure_index < 0 || arrival_index >= int(v_list.size()) || arrival_index < 0) throw out_of_range("can't push an edge with vertices not in the graph"); //petit test
        e_list.push_back(new edge(cost));
        v_list[departure_index]->push_neihghbour(v_list[arrival_index]);
        v_list[departure_index]->push_edge(e_list.back());
    }
}

void graph::build_scheduled_edges(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<int> departure_time, py::array_t<int> arrival_time, py::array_t<int> edge_id){
    int dep,arr;
    auto departure = departure_index.unchecked<1>();
    auto arrival = arrival_index.unchecked<1>();
    auto departure_t = departure_time.unchecked<1>();
    auto arrival_t = arrival_time.unchecked<1>();
    auto id = edge_id.unchecked<1>();
    assertm((departure.shape(0) == arrival.shape(0) && departure_t.shape(0) == arrival_t.shape(0) && arrival.shape(0) == departure_t.shape(0), departure_t.shape(0)==id.shape(0)),"departure_index ,arrival_index,departure_time,arrival_time must have same shape(0)" );
    for (int i = 0; i < departure.shape(0); i++) {
        push_scheduled_edge(int(departure(i)), int(arrival(i)), int(departure_t(i)), int(arrival_t(i)), int(id(i)));
    }
}
void graph::build_free_edges(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<int> cost ) {
    auto departure = departure_index.unchecked<1>();
    auto arrival = arrival_index.unchecked<1>();
    auto cost_w = cost.unchecked<1>();
    assertm((departure.shape(0) == arrival.shape(0) && cost.shape(0) == arrival.shape(0)), "departure_index, arrival_index,cost must have same shape(0)");
    for (int i = 0; i < departure.shape(0); i++) {
        push_free_edge(int(departure(i)), int(arrival(i)), int(cost_w(i)));
    }
}

void graph::build_scheduled_edges_string(py::array_t<int> departure_index, py::array_t<int> arrival_index, py::array_t<array<char,8>> departure_time, py::array_t<array<char,8>> arrival_time, py::array_t<int> edge_id){
    int dep, arr;
    auto departure = departure_index.unchecked<1>();
    auto arrival = arrival_index.unchecked<1>();
    auto departure_t = departure_time.unchecked<1>();
    auto arrival_t = arrival_time.unchecked<1>();
    auto id = edge_id.unchecked<1>();
    assertm((departure.shape(0) == arrival.shape(0) && departure_t.shape(0) == arrival_t.shape(0) && arrival.shape(0) == departure_t.shape(0), departure_t.shape(0) == id.shape(0)), "departure_index ,arrival_index,departure_time,arrival_time must have same shape(0)");
    for (int i = 0; i < departure.shape(0); i++) {
        push_scheduled_edge(int(departure(i)), int(arrival(i)), convert_seconds(departure_t.data(i)), convert_seconds(arrival_t.data(i)), int(id(i)));
    }

}


vertex* graph::operator[](int i){
    try { return v_list.at(i); }
    catch (out_of_range) { throw invalid_argument("This vertex is not in the graph"); } //conversion d'erreur , on veut une ValueError en pyhton = invalid_argument en cpp
}

void graph::initialised(){
    for (unsigned i = 0; i < v_list.size(); i++) {
        v_list[i]->time = inf;
        v_list[i]->visited = false;
    }
}

//alogorithms

void graph::basic_djikstra(int start_vertex_index) { // time independent
    //initialisation
    vertex* top = v_list[start_vertex_index];
    vertex* neighbour;
    int cost;
    top->time = 0;
    top->visited = true;
    priority_queue<vertex*, deque<vertex*>, comparetime> PQ; //definition de la file de prioritee avec le foncteur comparetime
    PQ.push(top);
    //boucle principale sur la taille de la file de prioritee
    while (!PQ.empty()) {
        //on retire le premier element de la file de priorite
        top = PQ.top();
        PQ.pop();
        //on explore ses voisins
        for (unsigned i = 0; i < top->number_neighbour(); i++) {
            neighbour = top->get_neighbour(i);          
            cost = top->time + top->cost_of_travel(i); // calcul du cout pour aller chez ce voisin depuis l'origine si le trajet passe par top . Dj basique independant du temps
            if (cost <= neighbour->time) {
                neighbour->time = cost;
                neighbour->predecessor = top;
            }
            if (neighbour->visited == false) { // si ce voisin n'est pas deja visite, (ie est deja sorti de la file de priorite et est donc deja atteint par l'algorithme
                neighbour->visited = true;
                PQ.push(neighbour);//on met ce voisin dans la file
            }
        }
    }
}

void graph::time_djikstra(int start_vertex_index, int t) { // time dependent
    //initialisation
    vertex* top = v_list[start_vertex_index];
    vertex* neighbour;
    int cost;
    top->time = t;
    top->visited = true ;
    priority_queue<vertex*, deque<vertex*>, comparetime> PQ; //definition de la file de prioritee avec le foncteur comparetime
    PQ.push(top);
    //boucle principale sur la taille de la file de prioritee
    while (!PQ.empty()) {
        //on retire le premier element de la file de priorite
        top = PQ.top();
        PQ.pop();
        //on explore ses voisins
        for (unsigned i = 0; i < top->number_neighbour(); i++) {
            neighbour = top->get_neighbour(i);
            cost = top->time + top->cost_of_travel(i,top->time); // calcul du cout pour aller chez ce voisin depuis l'origine si le trajet passe par top . dependant du temps
            if (cost <= neighbour->time) {
                neighbour->time = cost;
                neighbour->predecessor = top;
            }
            if (neighbour->visited == false) { // si ce voisin n'est pas deja visite, (ie est deja sorti de la file de priorite et est donc deja atteint par l'algorithme
                neighbour->visited = true;
                PQ.push(neighbour);//on met ce voisin dans la file
            }
        }
    }
}
void graph::stop_basic_djikstra(int start_vertex_index, int end_vertex_index){
    vertex* top = v_list[start_vertex_index];
    vertex* neighbour;
    int cost;
    top->time = 0;
    top->visited = true;
    priority_queue<vertex*, deque<vertex*>, comparetime> PQ; //definition de la file de prioritee avec le foncteur comparetime
    PQ.push(top);
    //boucle principale sur la taille de la file de prioritee
    while (!PQ.empty() && top->get_index()!= end_vertex_index) {
        //on retire le premier element de la file de priorite
        top = PQ.top(); //cout constant
        PQ.pop();//cout logaritmique
        //on explore ses voisins
        for (unsigned i = 0; i < top->number_neighbour(); i++) {
            neighbour = top->get_neighbour(i);
            // si ce voisin n'est pas deja visite, (ie est deja sorti de la file de priorite et est donc deja atteint par l'algorithme
            cost = top->time + top->cost_of_travel(i); // calcul du cout pour aller chez ce voisin depuis l'origine si le trajet passe par top . Dj basique independant du temps
            if (cost <= neighbour->time) {
                neighbour->time = cost;
                neighbour->predecessor = top;
            }
            if (neighbour->visited == false) {
                neighbour->visited = true;
                PQ.push(neighbour);//on met ce voisin dans la file //cout logaritmique
            }
        }
    }
}
void graph::stop_time_djikstra(int start_vertex_index, int end_vertex_index, int t ){
    vertex* top = v_list[start_vertex_index];
    vertex* neighbour;
    int cost;
    top->time = t;
    top->visited = true;
    priority_queue<vertex*, deque<vertex*>, comparetime> PQ; //definition de la file de prioritee avec le foncteur comparetime
    PQ.push(top);
    //boucle principale sur la taille de la file de prioritee
    while (!PQ.empty() && top->get_index() != end_vertex_index) {
        //on retire le premier element de la file de priorite
        top = PQ.top();
        PQ.pop();
        //on explore ses voisins
        for (unsigned i = 0; i < top->number_neighbour(); i++) {
            neighbour = top->get_neighbour(i);
            cost = top->time + top->cost_of_travel(i, top->time); // calcul du cout pour aller chez ce voisin depuis l'origine si le trajet passe par top . dependant du temps
            if (cost <= neighbour->time) {
                neighbour->time = cost;
                neighbour->predecessor = top;
            }
            if (neighbour->visited == false) { // si ce voisin n'est pas deja visite, (ie est deja sorti de la file de priorite et est donc deja atteint par l'algorithme
                neighbour->visited = true;
                PQ.push(neighbour);//on met ce voisin dans la file
            }
        }
    }
}
vector<int> graph::path_finder(int start_vertex_index, int end_vertex_index) {
    initialised();
    vector<int> path;
    stop_basic_djikstra(start_vertex_index, end_vertex_index);
    int index = end_vertex_index;
    while (index != start_vertex_index) {
        if (v_list[index]->visited == false) throw invalid_argument("no path found between start and end");
        path.push_back(index);
        index = v_list[index]->predecessor->get_index();
    }
    path.push_back(index);
    reverse(path.begin(), path.end());
    return path;

}
vector<int> graph::path_finder_time(int start_vertex_index, int end_vertex_index, int t){
    initialised();
    vector<int> path;
    stop_time_djikstra(start_vertex_index, end_vertex_index,t);
    int index = end_vertex_index;
    while (index != start_vertex_index) {
        if (v_list[index]->visited == false) throw invalid_argument("no path found between start and end");
        path.push_back(index);
        index = v_list[index]->predecessor->get_index();
    }
    path.push_back(index);
    reverse(path.begin(), path.end());
    return path;
}

vector<int> graph:: complete_path_finder(int start_vertex_index, int end_vertex_index) {
    initialised();
    vector<int> path;
    basic_djikstra(start_vertex_index);
    int index = end_vertex_index;
    while (index != start_vertex_index) {
        if (v_list[index]->visited == false) throw invalid_argument("no path found between start and end");
        path.push_back(index);
        index = v_list[index]->predecessor->get_index();
    }
    path.push_back(index);
    reverse(path.begin(), path.end());
    return path;
};
vector<int> graph::complete_path_finder_time(int start_vertex_index, int end_vertex_index, int t) {
    initialised();
    vector<int> path;
    time_djikstra(start_vertex_index, t);
    int index = end_vertex_index;
    while (index != start_vertex_index) {
        if (v_list[index]->visited == false) throw invalid_argument("no path found between start and end");
        path.push_back(index);
        index = v_list[index]->predecessor->get_index();
    }
    path.push_back(index);
    reverse(path.begin(), path.end());
    return path;
};
