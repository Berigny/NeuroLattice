import math
import numpy as np
import networkx as nx
from neuro_lattice.metrics import (
    calculate_strain,
    calculate_coherence,
    spectral_symmetry,
)


def build_lattice():
    g = nx.Graph()
    g.add_edge(0, 1, weight=1.0)
    g.add_edge(1, 2, weight=3.0)
    return g


def test_calculate_strain():
    g = build_lattice()
    assert calculate_strain(g) == 2.0


def test_calculate_coherence():
    g = build_lattice()
    expected = 1.0 / (1.0 + 1e-8)
    assert math.isclose(calculate_coherence(g), expected, rel_tol=1e-6)


def test_strain_threshold():
    g = build_lattice()
    assert calculate_strain(g) < 5.0


def test_coherence_threshold():
    g = build_lattice()
    assert calculate_coherence(g) > 0.5


def test_spectral_symmetry_eigvals():
    g = nx.complete_graph(5)
    eigvals, symmetry = spectral_symmetry(g)
    expected = np.sort(np.linalg.eigvalsh(nx.laplacian_matrix(g).toarray()))[: len(eigvals)]
    assert np.allclose(eigvals, expected)
    assert symmetry


def test_spectral_symmetry_non_degenerate():
    g = nx.path_graph(6)
    eigvals, symmetry = spectral_symmetry(g)
    expected = np.sort(np.linalg.eigvalsh(nx.laplacian_matrix(g).toarray()))[: len(eigvals)]
    assert np.allclose(eigvals, expected)
    assert not symmetry
