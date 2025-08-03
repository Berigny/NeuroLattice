import random
import networkx as nx
import pytest

from neuro_lattice.perturbations import PerturbationInjector

def test_adversarial_perturbation():
    G = nx.Graph()
    G.add_edge(1, 2, weight=1.0)
    PerturbationInjector().inject_perturbation(G, perturbation_type="adversarial")
    assert G[1][2]["weight"] == 5.0

def test_random_noise_perturbation():
    random.seed(0)
    G = nx.Graph()
    G.add_edge(1, 2, weight=1.0)
    PerturbationInjector().inject_perturbation(G, perturbation_type="random-noise")
    assert G[1][2]["weight"] == pytest.approx(1.3444218515250481)
