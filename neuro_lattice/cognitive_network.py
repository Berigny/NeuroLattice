"""Cognitive network construction.

This module wraps :class:`~neuro_lattice.lattice_builder.LatticeBuilder` and
annotates the resulting graph with per-node processing goals and confidence
thresholds. The thresholds are consumed by :class:`~neuro_lattice.routing_engine.RoutingEngine`
to model System 1 versus System 2 processing.
"""

from __future__ import annotations

import networkx as nx

from .lattice_builder import LatticeBuilder


class CognitiveNetwork:
    """Build and expose the cognitive lattice graph."""

    def __init__(self):
        builder = LatticeBuilder()
        self.graph: nx.DiGraph = builder.build_lattice()
        self._assign_goals()

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

        nx.set_node_attributes(self.graph, node_goals)

    # ------------------------------------------------------------------
    def get_network(self) -> nx.DiGraph:
        """Return the annotated network graph."""

        return self.graph

