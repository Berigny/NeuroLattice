class Packet:
    def __init__(self, data, routing_type):
        self.data = data
        self.routing_type = routing_type

class RoutingEngine:
    def __init__(self):
        self.routing_table = {}

    def add_route(self, destination, next_hop):
        self.routing_table[destination] = next_hop

    def route_packet(self, packet):
        if packet.routing_type == 'System 1':
            return self.system_1_routing(packet)
        elif packet.routing_type == 'System 2':
            return self.system_2_routing(packet)
        else:
            raise ValueError("Unknown routing type")

    def system_1_routing(self, packet):
        # Implement System 1 routing logic
        # For example, a simple direct routing
        return self.routing_table.get(packet.data['destination'], None)

    def system_2_routing(self, packet):
        # Implement System 2 routing logic
        # For example, a more complex decision-making process
        return self.routing_table.get(packet.data['destination'], None)

    def display_routes(self):
        for destination, next_hop in self.routing_table.items():
            print(f"Destination: {destination}, Next Hop: {next_hop}")