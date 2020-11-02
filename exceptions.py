
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
