import random
from collections import defaultdict

class RoutingEngine:
    def __init__(self, network):
        self.network = network
        self.visit_count = defaultdict(int, {n: 0 for n in self.network.nodes})
        self.transition_log = []
        self.ic_status = "up"
        self.goals = {n: {"threshold": 0.8, "confidence": 0.0} for n in self.network.nodes}

    def select_agent(self, node):
        if node in [0,1,2,3]: return "AgentA"
        if node in [4,5,6,7]: return "AgentB"
        if node == 'IC': return "AgentC1"
        if node == 'EC': return "AgentC2"

    def calculate_coherence(self, prev, new):
        edge_data = self.network.G.get_edge_data(prev, new)
        if not edge_data: return 0,0,3,1,0
        weight = edge_data.get('weight',1.0)
        strain = (1*weight) if (prev in [1,5] and new=='IC') else 0
        resonance = 1.2 if edge_data['type']=='tetrahedral' else 0.8
        distance = 1*weight
        p = self.network.primes.get(new,2)
        contrib = strain*resonance*(p**-distance)
        return strain,resonance,distance,p,contrib

    def decide_route(self, packet, successors):
        current = packet['location']
        if self.goals[current]["confidence"] < self.goals[current]["threshold"]:
            return 'IC' if 'IC' in successors else random.choice(successors)
        return random.choice(successors)
