"""Visualization utilities for NeuroLattice."""
import networkx as nx

def plot_lattice(lattice: nx.Graph, title: str = "Lattice Visualization"):
    """Draw the lattice graph using NetworkX spring layout."""
    import matplotlib.pyplot as plt

    pos = nx.get_node_attributes(lattice, "pos") or nx.spring_layout(lattice)
    nx.draw(lattice, pos, with_labels=True, node_color='skyblue', node_size=700,
            edge_color='gray', linewidths=1, font_size=12)
    plt.title(title)
    plt.show()
