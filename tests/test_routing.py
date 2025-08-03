from neuro_lattice.lattice_builder import LatticeBuilder
from neuro_lattice.routing_engine import RoutingEngine


def test_system_routing_moves_packet():
    lattice = LatticeBuilder().build_lattice()
    engine = RoutingEngine(lattice)
    packet = {"location": 0, "confidence": 0.5}
    updated = engine.route_packet(packet)
    assert updated["location"] != 0
