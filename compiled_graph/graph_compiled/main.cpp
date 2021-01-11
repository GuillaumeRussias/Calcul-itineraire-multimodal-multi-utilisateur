// cppimport
#include <pybind11/pybind11.h>
#include "graph.h"

namespace py = pybind11;

PYBIND11_MODULE(fast_graph, m){
    m.doc() = R"pbdoc(
        A compiled graph library : 3 classes vertex,edge,graph
    )pbdoc";

    py::class_<edge>(m, "edge")
            .def("type",&edge::get_type)
            .def("selected_mission",&edge::get_selected_mission)
            .def("transfers_cost",&edge::get_transfers_cost)
            .def("id",&edge::get_id)
            .def("print_missions",&edge::print_missions)
        ;
    py::class_<vertex>(m, "vertex")
            .def("__getitem__", &vertex::operator[], py::return_value_policy::reference)
            .def("neighbours",&vertex::get_neighbours)
            .def("time",&vertex::get_time)
            .def("visited",&vertex::get_visited)
            .def("predecessor",&vertex::get_predecessor)
        ;
    py::class_<graph>(m, "graph")
            .def(py::init<int>())
            .def("build_scheduled_edges", &graph::build_scheduled_edges)
            .def("build_scheduled_edges_string",&graph::build_scheduled_edges_string)
            .def("build_free_edges", &graph::build_free_edges)
            .def("__getitem__", &graph::operator[], py::return_value_policy::reference)
            .def("basic_path_finder",&graph::path_finder)
            .def("time_path_finder",&graph::path_finder_time)
            .def("complete_basic_path_finder", &graph::complete_path_finder)
            .def("complete_time_path_finder", &graph::complete_path_finder_time)
            .def("multi_users_dijkstra", &graph::multi_users_dijkstra)


        ;
}
