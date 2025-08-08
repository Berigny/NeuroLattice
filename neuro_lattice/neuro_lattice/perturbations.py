import random
import networkx as nx

class PerturbationInjector:
    """Minimal perturbation helper for tests."""

    def inject_perturbation(self, lattice: nx.Graph, perturbation_type: str = "adversarial"):
        """Apply different perturbations to the first edge of the lattice.

        Parameters
        ----------
        lattice:
            Graph whose first edge will be perturbed. If the graph has no
            edges, it is returned unchanged.
        perturbation_type:
            The type of perturbation to apply. Supported values are
            "adversarial" and "random-noise".
        """
        if lattice.number_of_edges() == 0:
            return lattice

        # Grab the first edge and its data dictionary. This keeps the helper
        # deterministic and easy to reason about for tests.
        edge = next(iter(lattice.edges(data=True)))
        data = edge[2]
        weight = data.get("weight", 1.0)

        if perturbation_type == "adversarial":
            # Dramatically increase the weight to simulate an adversarial
            # manipulation of the edge cost.
            data["weight"] = weight * 5
        elif perturbation_type == "random-noise":
            # Inject bounded random noise into the weight. The magnitude is
            # intentionally small so tests can seed the RNG and assert exact
            # values.
            data["weight"] = weight + random.uniform(-0.5, 0.5)
        else:
            raise ValueError(f"Unsupported perturbation_type: {perturbation_type}")

        return lattice
