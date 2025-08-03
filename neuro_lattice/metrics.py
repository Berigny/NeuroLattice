import numpy as np
import networkx as nx

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
    return compute_strain(lattice)


def _calculate_drift(lattice):
    """Simple drift metric based on deviation of mean edge weight from 1."""
    weights = [d.get("weight", 1.0) for _, _, d in lattice.edges(data=True)]
    return abs(np.mean(weights) - 1.0)


class MetricsCalculator:
    """Utility class for collecting core lattice metrics."""

    @staticmethod
    def calculate_metrics(lattice):
        return {
            "strain": compute_strain(lattice),
            "coherence": compute_coherence(lattice),
            "drift": _calculate_drift(lattice),
        }

def node_visit_imbalance(visit_counts):
    """
    Imbalance = max node visits / mean visits.
    """
    if not visit_counts:
        return 0.0
    visits = np.array(list(visit_counts.values()))
    return visits.max() / (visits.mean() + 1e-8)

def spectral_symmetry(lattice):
    """
    Checks for Laplacian eigenvalue degeneracy (structural symmetry).
    Returns (eigenvalues, symmetry_passed).
    """
    L = nx.laplacian_matrix(lattice).toarray()
    eigvals = np.sort(np.linalg.eigvalsh(L))
    symmetry = np.isclose(eigvals[1:4], eigvals[1], atol=1e-12)
    return eigvals, symmetry.all()

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
