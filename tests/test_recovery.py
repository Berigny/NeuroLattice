import networkx as nx
from neuro_lattice import PerturbationEngine
from neuro_lattice.metrics import MetricsCalculator


def create_test_lattice():
    g = nx.Graph()
    g.add_edge(0, 1, weight=1.0)
    g.add_edge(1, 2, weight=1.0)
    return g


def recover_lattice(lattice):
    for _, _, data in lattice.edges(data=True):
        data["weight"] = 1.0


def test_recovery_mechanism():
    lattice = create_test_lattice()
    injector = PerturbationEngine()
    injector.inject_perturbation(lattice, perturbation_type="adversarial")
    metrics_before = MetricsCalculator.calculate_metrics(lattice)
    recover_lattice(lattice)
    metrics_after = MetricsCalculator.calculate_metrics(lattice)
    assert metrics_after["strain"] < metrics_before["strain"]
    assert metrics_after["coherence"] > metrics_before["coherence"]
    assert metrics_after["drift"] < metrics_before["drift"]
