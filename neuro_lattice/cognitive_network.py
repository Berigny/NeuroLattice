from __future__ import annotations
from typing import Iterable, List, Dict, Any
import networkx as nx

from .lattice_builder import LatticeBuilder
from .routing_engine import RoutingEngine


class CognitiveNetwork:
    """Construct and interact with a cognitive lattice.

    Parameters
    ----------
    lattice_type:
        Shape of lattice to build. Currently ``'tetrahedral'`` or ``'cubic'``.
    size:
        Scaling factor for node positions and edge weights in the lattice.
    """

    def __init__(self, lattice_type: str = "tetrahedral", size: float = 1.0) -> None:
        self.builder = LatticeBuilder(lattice_type=lattice_type, size=size)
        self.network: nx.DiGraph = self.builder.build_lattice()
        self._assign_goals()
        self.router = RoutingEngine(self.network)

    # ------------------------------------------------------------------
    def _assign_goals(self) -> None:
        """Assign processing goals and confidence thresholds to nodes."""
        node_goals = {
            0: {"goal": "fast_reading", "threshold": 0.5},
            1: {"goal": "coarse_eval", "threshold": 0.6},
            2: {"goal": "pattern_match", "threshold": 0.7},
            3: {"goal": "fast_decision", "threshold": 0.8},
            4: {"goal": "deep_reading", "threshold": 0.85},
            5: {"goal": "integration", "threshold": 0.9},
            6: {"goal": "critical_eval", "threshold": 0.95},
            7: {"goal": "deliberate_decision", "threshold": 0.95},
            "IC": {"goal": "integration_hub", "threshold": 1.0},
            "EC": {"goal": "entry_exit", "threshold": 0.0},
        }
        nx.set_node_attributes(self.network, node_goals)

    # ------------------------------------------------------------------
    def get_network(self) -> nx.DiGraph:
        """Return the underlying annotated network."""
        return self.network

    def set_lattice_parameters(self, lattice_type: str, size: float) -> None:
        """Rebuild the lattice with new parameters."""
        self.builder.set_lattice_parameters(lattice_type, size)
        self.network = self.builder.build_lattice()
        self._assign_goals()
        self.router = RoutingEngine(self.network)

    def route_packets(self, packets: Iterable[Dict[str, Any]], max_steps: int = 100) -> List[Dict[str, Any]]:
        """Route packets through the lattice via :class:`~neuro_lattice.routing_engine.RoutingEngine`."""
        return self.router.run(packets, max_steps=max_steps)
