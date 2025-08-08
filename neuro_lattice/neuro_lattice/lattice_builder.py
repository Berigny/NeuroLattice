import math
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
        nodes = list(range(8)) + ["IC", "EC"]
        G.add_nodes_from(nodes)

        # Base coordinates for two tetrahedra and centroids
        base_pos = {
            0: (0.0, 0.0, 0.0),
            1: (1.0, 0.0, 0.0),
            2: (0.0, 1.0, 0.0),
            3: (0.0, 0.0, 1.0),
            4: (1.0, 1.0, 1.0),
            5: (2.0, 1.0, 1.0),
            6: (1.0, 2.0, 1.0),
            7: (1.0, 1.0, 2.0),
            "IC": (0.5, 0.5, 0.5),
            "EC": (1.5, 1.5, 1.5),
        }

        # Scale coordinates by lattice size
        pos = {n: (x * self.size, y * self.size, z * self.size) for n, (x, y, z) in base_pos.items()}
        nx.set_node_attributes(G, pos, "pos")

        # Tetrahedron 1 (0-3) and Tetrahedron 2 (4-7)
        tetra1 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        tetra2 = [(4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
        G.add_edges_from(tetra1 + tetra2)

        # Cross edges (connect tetrahedra)
        cross_edges = [(0, 4), (1, 5), (2, 6), (3, 7)]
        G.add_edges_from(cross_edges)

        # Centroid connections
        centroid_edges = [
            ("EC", "IC"), ("EC", 0), ("EC", 4),
            (0, "EC"), (4, "EC"), (6, "EC"), (7, "EC"),
        ]
        G.add_edges_from(centroid_edges)

        # Assign edge weights based on Euclidean distance
        for u, v in G.edges():
            p1, p2 = pos[u], pos[v]
            G.edges[u, v]["weight"] = math.dist(p1, p2)

        return G

    def _build_cubic_lattice(self):
        # Nodes in grid_3d_graph are coordinates (x, y, z)
        base = nx.grid_3d_graph(2, 2, 2)

        # Convert to directed graph with bidirectional edges
        base = base.to_directed()

        # Map coordinate nodes to integer labels while storing positions
        mapping = {node: i for i, node in enumerate(base.nodes())}
        pos = {mapping[node]: (node[0] * self.size, node[1] * self.size, node[2] * self.size) for node in base.nodes()}

        G = nx.relabel_nodes(base, mapping, copy=True)
        nx.set_node_attributes(G, pos, "pos")

        # Assign edge weights
        for u, v in G.edges():
            p1, p2 = pos[u], pos[v]
            G.edges[u, v]["weight"] = math.dist(p1, p2)

        return G

    def set_lattice_parameters(self, lattice_type, size):
        self.lattice_type = lattice_type
        self.size = size

    def get_lattice(self):
        return self.lattice
