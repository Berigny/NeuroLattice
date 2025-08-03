import pytest
from neuro_lattice.routing_engine import RoutingEngine

def test_system_1_routing():
    routing_engine = RoutingEngine()
    packet = {'source': 'A', 'destination': 'B', 'type': 'system_1'}
    route = routing_engine.route_packet(packet)
    
    assert route is not None
    assert 'A' in route
    assert 'B' in route
    assert route.index('A') < route.index('B')

def test_system_2_routing():
    routing_engine = RoutingEngine()
    packet = {'source': 'C', 'destination': 'D', 'type': 'system_2'}
    route = routing_engine.route_packet(packet)
    
    assert route is not None
    assert 'C' in route
    assert 'D' in route
    assert route.index('C') < route.index('D')

def test_invalid_packet_routing():
    routing_engine = RoutingEngine()
    packet = {'source': 'E', 'destination': 'F', 'type': 'invalid_type'}
    route = routing_engine.route_packet(packet)
    
    assert route is None

def test_routing_with_perturbations():
    routing_engine = RoutingEngine()
    packet = {'source': 'G', 'destination': 'H', 'type': 'system_1'}
    routing_engine.apply_perturbation({'type': 'delay', 'amount': 5})
    route = routing_engine.route_packet(packet)
    
    assert route is not None
    assert 'G' in route
    assert 'H' in route
    assert route.index('G') < route.index('H')