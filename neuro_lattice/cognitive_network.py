"""High-level interface for building and simulating cognitive lattices."""

from __future__ import annotations

from typing import Iterable, List, Dict, Any

from .lattice_builder import LatticeBuilder
from .routing_engine import RoutingEngine


class CognitiveNetwork:
    """Construct and interact with a cognitive lattice.

    Parameters
    ----------
    lattice_type:
        Shape of lattice to build. Currently ``'tetrahedral'`` or ``'cubic'``.
    size:
        Scaling factor passed to :class:`~neuro_lattice.lattice_builder.LatticeBuilder`.
    """

    def __init__(self, lattice_type: str = "tetrahedral", size: float = 1.0) -> None:
        self.builder = LatticeBuilder(lattice_type=lattice_type, size=size)
        self.network = self.builder.build_lattice()
        self.router = RoutingEngine(self.network)

    def get_network(self):
        """Return the underlying :class:`networkx.Graph` instance."""
        return self.network

    def set_lattice_parameters(self, lattice_type: str, size: float) -> None:
        """Rebuild the lattice with new parameters."""
        self.builder.set_lattice_parameters(lattice_type, size)
        self.network = self.builder.build_lattice()
        self.router = RoutingEngine(self.network)

    def route_packets(self, packets: Iterable[Dict[str, Any]], max_steps: int = 100) -> List[Dict[str, Any]]:
        """Route packets through the lattice via :class:`~neuro_lattice.routing_engine.RoutingEngine`."""
        return self.router.run(packets, max_steps=max_steps)
