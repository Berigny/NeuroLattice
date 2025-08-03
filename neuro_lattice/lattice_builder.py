import networkx as nx

class LatticeBuilder:
    def __init__(self, lattice_type='tetrahedral', size=1.0):
        self.lattice_type = lattice_type
        self.size = size
        self.lattice = None

    def build_lattice(self):
        if self.lattice_type == 'tetrahedral':
            self.lattice = self._build_tetrahedral_lattice()
        elif self.lattice_type == 'cubic':
            self.lattice = self._build_cubic_lattice()
        else:
            raise ValueError("Unsupported lattice type. Choose 'tetrahedral' or 'cubic'.")
        return self.lattice

    def _build_tetrahedral_lattice(self):
        G = nx.DiGraph()
        nodes = list(range(8)) + ['IC', 'EC']  # 8 lattice nodes + internal/external centroids
        G.add_nodes_from(nodes)

        # Tetrahedron 1 (0-3)
        tetra1 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        # Tetrahedron 2 (4-7)
        tetra2 = [(4,5),(4,6),(4,7),(5,6),(5,7),(6,7)]
        G.add_edges_from(tetra1 + tetra2)

        # Cross edges (connect tetrahedra)
        cross_edges = [(0,4),(1,5),(2,6),(3,7)]
        G.add_edges_from(cross_edges)

        # Centroid connections
        centroid_edges = [
            ('EC','IC'), ('EC',0), ('EC',4),
            (0,'EC'), (4,'EC'), (6,'EC'), (7,'EC')
        ]
        G.add_edges_from(centroid_edges)

        return G

    def _build_cubic_lattice(self):
        G = nx.grid_3d_graph(2, 2, 2)  # basic 2x2x2 cube lattice
        return nx.convert_node_labels_to_integers(G)

    def set_lattice_parameters(self, lattice_type, size):
        self.lattice_type = lattice_type
        self.size = size

    def get_lattice(self):
        return self.lattice
