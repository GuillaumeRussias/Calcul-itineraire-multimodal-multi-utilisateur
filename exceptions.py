import pkg_resources
def check_pertinent_edge(vertice, edge):
    if edge.linked[0] != vertice:
        raise Non_pertinent_Edge(vertice, edge)

def check_pertinent_edge_coords_verif(vertice, edge):
    if edge.linked[0].coordinates[0] != vertice.coordinates[0] or edge.linked[0].coordinates[1]!=vertice.coordinates[1]:
        raise Non_pertinent_Edge(vertice, edge)

class Non_pertinent_Edge(Exception):
    def __init__(self, vertice, edge):
        super().__init__()
        self._non_pertinent_Edge = edge
        self._vertice = vertice
        self.message = f"It's not pertinent to put this edge : {repr(self._non_pertinent_Edge)} in list of edges of the vertice : {repr(self._vertice)}"


class compiled_graph_version_error(Exception):
    def __init__(self, current_version, newest_version):
        super().__init__()
        self._current_version = current_version
        self._newest_version = newest_version
        self.message = f"The current version of compiled_graph library : {self._current_version} is not up to date, please install the newest version : {self._newest_version} with pip install ./compiled_graph"
    def __str__(self):
        return self.message 

def check_compiled_graph_version(newest_version):
    current_version = pkg_resources.get_distribution('fast_graph').version
    if current_version!= newest_version :
        raise compiled_graph_version_error(current_version,newest_version)
