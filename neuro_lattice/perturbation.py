import random
import networkx as nx
import numpy as np

class PerturbationEngine:
    """
    Injects controlled noise, drift, or failures into the lattice
    to test robustness and recovery.
    """
    def __init__(self, lattice):
        self.lattice = lattice

    def random_edge_drop(self, drop_fraction=0.1):
        """Randomly remove a fraction of edges."""
        edges = list(self.lattice.edges())
        n_drop = max(1, int(len(edges) * drop_fraction))
        to_remove = random.sample(edges, n_drop)
        self.lattice.remove_edges_from(to_remove)
        return to_remove

    def random_weight_noise(self, noise_level=0.2):
        """Add Gaussian noise to edge weights."""
        for u, v, data in self.lattice.edges(data=True):
            if "weight" in data:
                noise = np.random.normal(0, noise_level)
                data["weight"] = max(0.1, data["weight"] + noise)

    def data_poisoning(self, node_attr="goal", corruption_rate=0.2):
        """Corrupts node attributes to simulate bad data."""
        for node in self.lattice.nodes():
            if random.random() < corruption_rate:
                self.lattice.nodes[node][node_attr] = "CORRUPTED"

    def reset_lattice(self, builder):
        """Rebuilds the lattice to its original clean state."""
        self.lattice = builder.build_lattice()
        return self.lattice
