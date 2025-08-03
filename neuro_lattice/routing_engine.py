import random
import networkx as nx
from collections import defaultdict

class RoutingEngine:
    """
    Routes packets through the lattice.
    Each node has a 'goal' and packets carry 'confidence'.
    """
    def __init__(self, lattice):
        self.lattice = lattice
        self.visit_counts = defaultdict(int)
        self.transition_log = []

    def _select_agent(self, node):
        # Example: Map tetrahedral subsets to agents
        if node in [0,1,2,3]: return "AgentA"
        if node in [4,5,6,7]: return "AgentB"
        if node == "IC": return "AgentC1"
        if node == "EC": return "AgentC2"
        return "Unknown"

    def _goal_reached(self, node, packet):
        """
        Check if a node's goal is reached for the packet.
        """
        goal = self.lattice.nodes[node].get("goal", None)
        if not goal:
            return False
        # Simple logic: if packet has >= required confidence
        return packet['confidence'] >= self.lattice.nodes[node].get("goal_threshold", 0.8)

    def decide_next(self, current, packet):
        """
        Decide next node based on:
        - Goal completion (move toward EC if done)
        - Otherwise: random successor
        """
        successors = list(self.lattice.successors(current))
        if not successors:
            return None

        # If this node achieved its goal, route toward EC
        if self._goal_reached(current, packet):
            if "EC" in successors:
                return "EC"
            # If no direct EC, prefer path closer to EC
            paths = [(s, nx.shortest_path_length(self.lattice, s, "EC")) for s in successors if nx.has_path(self.lattice, s, "EC")]
            if paths:
                return min(paths, key=lambda x: x[1])[0]

        # Otherwise, pick a random neighbor
        return random.choice(successors)

    def route_packet(self, packet):
        """
        Move a packet one step and update its confidence.
        """
        current = packet['location']
        next_node = self.decide_next(current, packet)
        if next_node is None:
            return packet  # Dead-end, stay

        # Log transition
        self.transition_log.append({
            'agent': self._select_agent(current),
            'from': current,
            'to': next_node,
            'confidence': packet['confidence']
        })

        # Update packet
        packet['location'] = next_node
        # Confidence adjustment: Increase if moving to IC (reflection), decrease otherwise
        if next_node == "IC":
            packet['confidence'] = min(1.0, packet['confidence'] + 0.1)
        else:
            packet['confidence'] = max(0.0, packet['confidence'] - 0.05)

        # Track visits
        self.visit_counts[next_node] += 1
        return packet

    def run(self, packets, max_steps=100):
        """
        Simulate routing until all packets reach EC or steps exhausted.
        """
        for _ in range(max_steps):
            for p in packets:
                if p['location'] != "EC":
                    self.route_packet(p)
        return packets
