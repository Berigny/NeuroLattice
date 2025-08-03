import random

import pytest

from neuro_lattice.cognitive_network import CognitiveNetwork
from neuro_lattice.routing_engine import RoutingEngine


def _make_packet(location, confidence):
    return {
        "id": 0,
        "data": "",
        "location": location,
        "prev": None,
        "priority": 1.0,
        "confidence": confidence,
    }


def test_system2_holds_packet_until_confident():
    network = CognitiveNetwork().get_network()
    engine = RoutingEngine(network)
    random.seed(0)

    packet = _make_packet(location=4, confidence=0.8)  # threshold for 4 is 0.85

    engine.route_packet(packet)
    assert packet["location"] == 4  # still in System 2 node
    assert packet["confidence"] == pytest.approx(0.85)
    entry = engine.transition_log[-1]
    assert entry["from"] == entry["to"] == 4
    assert entry["confidence_before"] == pytest.approx(0.8)
    assert entry["confidence_after"] == pytest.approx(0.85)

    # Next step should move now that confidence >= threshold
    engine.route_packet(packet)
    assert packet["location"] != 4
    assert packet["confidence"] >= 0.85


def test_system1_moves_even_if_below_threshold():
    network = CognitiveNetwork().get_network()
    engine = RoutingEngine(network)
    random.seed(0)

    packet = _make_packet(location=0, confidence=0.4)  # threshold for 0 is 0.5

    engine.route_packet(packet)
    assert packet["location"] != 0  # System 1 nodes don't hold packets

