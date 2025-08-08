import matplotlib.pyplot as plt
import networkx as nx

def plot_lattice(lattice, title="Lattice Visualization"):
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(lattice)
    nx.draw(lattice, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', linewidths=1, font_size=15)
    plt.title(title)
    plt.show()

def plot_routing_paths(paths, title="Routing Paths Visualization"):
    plt.figure(figsize=(10, 10))
    for path in paths:
        nx.draw_networkx_edges(path['graph'], pos=path['positions'], edgelist=path['edges'], width=2)
    plt.title(title)
    plt.show()

def plot_metrics(metrics, title="Performance Metrics"):
    plt.figure(figsize=(10, 5))
    plt.plot(metrics['x'], metrics['y'], marker='o')
    plt.title(title)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.grid()
    plt.show()