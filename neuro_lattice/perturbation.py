"""Utilities for injecting perturbations into lattices.

This module exposes :class:`PerturbationEngine` as the single public
interface for applying noise, edge drops, or other fault injection
strategies to lattice graphs.
"""

import random
import numpy as np

class PerturbationEngine:
    """
    Injects controlled noise, drift, or failures into a lattice to
    test robustness and recovery.

    This class supersedes the former ``PerturbationInjector`` helper by
    providing a single interface for applying lightweight perturbations as
    well as more involved fault injection strategies.
    """

    def __init__(self, lattice=None):
        self.lattice = lattice

    def inject_perturbation(self, lattice=None, perturbation_type="adversarial"):
        """Apply a simple weight perturbation to an edge in the lattice.

        Parameters
        ----------
        lattice : nx.Graph, optional
            The lattice to perturb. If ``None``, the instance's lattice is used.
        perturbation_type : str, default "adversarial"
            Placeholder for future perturbation categories.
        """
        target = lattice or self.lattice
        if target is None or target.number_of_edges() == 0:
            return target
        edge = next(iter(target.edges(data=True)))
        data = edge[2]
        data["weight"] = data.get("weight", 1.0) * 5
        return target

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
