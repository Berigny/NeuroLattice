import numpy as np
import networkx as nx
from scipy.sparse.linalg import eigsh

def compute_coherence(lattice):
    """
    Compute coherence as the inverse variance of edge weights.
    Higher = more coherent.
    """
    weights = [d.get("weight", 1.0) for _, _, d in lattice.edges(data=True)]
    return 1.0 / (np.var(weights) + 1e-8)

def compute_strain(lattice):
    """
    Strain = sum of deviations of edge weights from their mean.
    """
    weights = [d.get("weight", 1.0) for _, _, d in lattice.edges(data=True)]
    mean_weight = np.mean(weights)
    return sum(abs(w - mean_weight) for w in weights)


def calculate_coherence(lattice):
    """Public wrapper for :func:`compute_coherence`."""
    return compute_coherence(lattice)


def calculate_strain(lattice):
    """Public wrapper for :func:`compute_strain`."""


class MetricsCalculator:
    """Utility class for collecting core lattice metrics."""

    @staticmethod
    def calculate_metrics(lattice):
        return {
            "strain": compute_strain(lattice),
            "coherence": compute_coherence(lattice),
            # "drift": _calculate_drift(lattice),  # Removed undefined function
        }

def node_visit_imbalance(visit_counts):
    """
    Imbalance = max node visits / mean visits.
    """
    visits = np.array(list(visit_counts.values()))
    return visits.max() / (visits.mean() + 1e-8)

def spectral_symmetry(lattice):
    """
    Checks for Laplacian eigenvalue degeneracy (structural symmetry).
    Returns (eigenvalues, symmetry_passed).
    """
    L = nx.laplacian_matrix(lattice)
    num_eigs = min(L.shape[0] - 1, 10)
    if num_eigs <= 0:
        return np.array([]), True
    eigvals = np.sort(eigsh(L, k=num_eigs, which="SA", return_eigenvectors=False))
    symmetry = len(eigvals) >= 4 and np.isclose(eigvals[1:4], eigvals[1], atol=1e-12).all()
    return eigvals, symmetry

def coherence_report(lattice, visit_counts):
    """
    Returns a dictionary with all core metrics.
    """
    eigvals, symmetry = spectral_symmetry(lattice)
    return {
        "coherence": compute_coherence(lattice),
        "strain": compute_strain(lattice),
        "imbalance": node_visit_imbalance(visit_counts),
        "spectral_symmetry_ok": symmetry,
        "laplacian_eigs": eigvals[:10]  # First 10 eigenvalues for debugging
    }