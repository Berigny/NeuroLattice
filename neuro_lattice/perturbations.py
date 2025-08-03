import networkx as nx

class PerturbationInjector:
    """Minimal perturbation helper for tests."""

    def inject_perturbation(self, lattice: nx.Graph, perturbation_type: str = "adversarial"):
        """Apply a simple weight perturbation to an edge in the lattice."""
        if lattice.number_of_edges() == 0:
            return lattice
        edge = next(iter(lattice.edges(data=True)))
        data = edge[2]
        data["weight"] = data.get("weight", 1.0) * 5
        return lattice
