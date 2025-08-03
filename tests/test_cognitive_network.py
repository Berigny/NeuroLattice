from neuro_lattice import CognitiveNetwork


def test_cognitive_network_basic():
    network = CognitiveNetwork()
    network.add_concept("A")
    network.add_concept("B")
    network.add_relation("A", "B", weight=0.5)

    adj = network.adjacency_matrix()

    assert adj.shape == (2, 2)
    assert adj[0, 1] == 0.5
