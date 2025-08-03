"""Cognitive network utilities.

This module defines a minimal :class:`CognitiveNetwork` used throughout the
project.  It provides a lightweight wrapper around a directed NetworkX graph
so that experiments can easily add concepts and relationships between them.

The original repository only shipped an empty placeholder file which caused
imports such as ``from neuro_lattice import CognitiveNetwork`` to fail at
runtime.  The implementation below establishes a small but functional API that
is sufficient for tests and examples while remaining simple.
"""

from __future__ import annotations

from typing import Any

import networkx as nx


class CognitiveNetwork:
    """A basic directed network of concepts and their relationships.

    Concepts are represented as nodes in a :class:`networkx.DiGraph` and
    relationships are stored as weighted edges.  The class exposes convenience
    methods for adding concepts and relations as well as retrieving the
    underlying adjacency matrix for analysis.
    """

    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_concept(self, concept: Any) -> None:
        """Add a concept node to the network."""

        self.graph.add_node(concept)

    def add_relation(self, source: Any, target: Any, weight: float = 1.0) -> None:
        """Create a weighted directed relation between two concepts."""

        self.graph.add_edge(source, target, weight=weight)

    def adjacency_matrix(self):
        """Return the adjacency matrix of the cognitive network."""

        return nx.to_numpy_array(self.graph, weight="weight")

