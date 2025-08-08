import pandas as pd
import matplotlib.pyplot as plt
from .vision_agent import VisionAgent
from .cognitive_network import CognitiveNetwork
from .routing_engine import RoutingEngine

class Simulation:
    def __init__(self):
        self.vision = VisionAgent()
        self.network = CognitiveNetwork()
        self.controller = RoutingEngine(self.network)
        self.packets = []

    def initialize(self, image):
        shapes = self.vision.detect_shapes(image)
        description = f"Detected shapes: {', '.join(shapes)}"
        self.packets = [{'id':0,'data':description,'location':'EC','prev':None,'priority':1.0 if shapes else 0.5}]

    def run_step(self, verbose=False):
        new_packets = []
        for p in self.packets:
            prev = p['location']
            successors = list(self.network.G.successors(prev))
            if not successors: 
                new_packets.append(p)
                continue
            new_loc = self.controller.decide_route(p, successors)
            metrics = self.controller.calculate_coherence(prev,new_loc)
            self.controller.transition_log.append({
                'agent':self.controller.select_agent(prev),'from':prev,'to':new_loc,
                'strain':metrics[0],'resonance':metrics[1],'distance':metrics[2],
                'prime':metrics[3],'contrib':metrics[4]
            })
            p['prev'] = prev
            p['location'] = new_loc
            new_packets.append(p)
            self.controller.visit_count[new_loc]+=1
        self.packets = new_packets

    def calculate_coherence(self):
        if not self.controller.transition_log: return 1.0
        total = sum(t['contrib'] for t in self.controller.transition_log)
        return (total/len(self.controller.transition_log))+1

    def visualize(self):
        self.network.visualize([p['location'] for p in self.packets])
        plt.figure(figsize=(10,5))
        visits = sorted([(str(k),v) for k,v in self.controller.visit_count.items()])
        plt.bar([k for k,v in visits],[v for k,v in visits])
        plt.title("Node Visit Distribution")
        plt.xlabel("Node")
        plt.ylabel("Visit Count")
        plt.show()
