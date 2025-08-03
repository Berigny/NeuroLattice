import networkx as nx
from neuro_lattice import CognitiveNetwork


def test_cognitive_network_basic():
    cn = CognitiveNetwork(lattice_type="tetrahedral", size=1.0)
    graph = cn.get_network()

    # Graph should be a directed graph with the expected number of nodes
    assert isinstance(graph, nx.DiGraph)
    assert len(graph) == 10

    # Node positions should be available from the builder
    assert graph.nodes[1]["pos"] == (1.0, 0.0, 0.0)
