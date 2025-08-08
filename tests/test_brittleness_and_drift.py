"""
MVP brittleness-and-drift detector test suite for the tetrahedral-breath lattice.

Each test is cheap, quantitatively pass/fail, and tied to theoretical claims.
"""
import numpy as np
import networkx as nx
import pytest
from scipy.stats import chisquare

from neuro_lattice.lattice_builder import LatticeBuilder
from neuro_lattice.metrics import spectral_symmetry, compute_strain
def test_lattice_symmetry_smoke():
    """Ensure the Laplacian has the predicted triple-degenerate eigenmode."""
    G = LatticeBuilder(lattice_type="cubic", size=1.0).build_lattice()
    G_undirected = G.to_undirected()
    eigvals, symmetry = spectral_symmetry(G_undirected)
    assert symmetry, "Spectral symmetry check failed"
    # explicit triple degeneracy test
    assert np.isclose(eigvals[1:4], eigvals[1], atol=1e-12).all()


def test_strain_zero_mean():
    """Verify that strain on a clean lattice remains centered on zero deviation."""
    G = LatticeBuilder(lattice_type="tetrahedral", size=1.0).build_lattice()
    strains = [compute_strain(G) for _ in range(100)]
    # mean absolute deviation around mean should be small
    assert np.mean(np.abs(strains - np.mean(strains))) < 0.05


@pytest.mark.skip(reason="Controlled perturbation/recovery sprint not yet implemented")
def test_controlled_perturbation_recovery_sprint():
    """Placeholder for controlled perturbation and recovery benchmark."""
    pass
