import networkx as nx

def initialise_lattice(kernel_data):
    G = nx.Graph()
    for system, nodes in kernel_data['brand_identity_kernel']['core_nodes'].items():
        for node, description in nodes.items():
            G.add_node(f"{system}-{node}", description=description)
    return G
