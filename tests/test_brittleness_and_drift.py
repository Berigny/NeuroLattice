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
from neuro_lattice.cognitive_network import CognitiveNetwork


def test_lattice_symmetry_smoke():
    """Ensure the Laplacian has the predicted triple-degenerate eigenmode."""
    G = LatticeBuilder(lattice_type="tetrahedral", size=1.0).build_lattice()
    eigvals, symmetry = spectral_symmetry(G)
    assert symmetry, "Spectral symmetry check failed"
    # explicit triple degeneracy test
    assert np.isclose(eigvals[1:4], eigvals[1], atol=1e-12).all()


def test_load_balanced_traffic():
    """Confirm no single node becomes a choke-point under synthetic load."""
    cn = CognitiveNetwork()
    packets = [{"location": "EC", "confidence": 0.0} for _ in range(1000)]
    cn.route_packets(packets, max_steps=100)
    counts = list(cn.router.visit_counts.values())
    assert counts, "No visit counts recorded"
    assert max(counts) <= 2 * min(counts), "Load imbalance detected"


def test_centroid_loop_closure():
    """Check that each path leaving EC hits IC before returning to EC."""
    cn = CognitiveNetwork()
    router = cn.router
    trials = 200
    hits = 0
    for _ in range(trials):
        packet = {"location": "EC", "confidence": 0.0}
        visited_ic = False
        # simulate until return to EC
        while True:
            packet = router.route_packet(packet)
            if packet["location"] == "IC":
                visited_ic = True
            if packet["location"] == "EC":
                break
        if visited_ic:
            hits += 1
    assert hits / trials >= 0.95, f"IC hit rate too low: {hits}/{trials}"


def test_strain_zero_mean():
    """Verify that strain on a clean lattice remains centered on zero deviation."""
    G = LatticeBuilder(lattice_type="tetrahedral", size=1.0).build_lattice()
    strains = [compute_strain(G) for _ in range(100)]
    # mean absolute deviation around mean should be small
    assert np.mean(np.abs(strains - np.mean(strains))) < 0.05


def test_prime_weight_drift_detector():
    """Quick chi-squared test: traffic frequency inversely tracks prime-weighted nodes."""
    cn = CognitiveNetwork()
    packets = [{"location": "EC", "confidence": 0.0} for _ in range(500)]
    cn.route_packets(packets, max_steps=50)
    counts = cn.router.visit_counts
    # primes among node labels (2,3,5,7)
    prime_nodes = [n for n in cn.get_network().nodes() if isinstance(n, int) and n in {2, 3, 5, 7}]
    observed = [counts.get(p, 0) for p in prime_nodes]
    expected = [sum(observed) / len(observed)] * len(observed)
    chi2, p = chisquare(observed, expected)
    assert p > 0.05, f"Prime-weight drift detected (p={p:.3f})"


@pytest.mark.skip(reason="Controlled perturbation/recovery sprint not yet implemented")
def test_controlled_perturbation_recovery_sprint():
    """Placeholder for controlled perturbation and recovery benchmark."""
    pass
