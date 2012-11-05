from algorithm import RoutingAlgorithm
from device import Device
from router import Router

class BellmanFord(RoutingAlgorithm):
    """
    """

    _COSTS = 'costs'

    # Overrides Algorithm.initialize(router)
    def initialize(self, router):
        """
        Initializes the routing algorithm using the specified router.
        """

        # Checks that router is a Router instance
        if not isinstance(router, Router):
            raise TypeError, 'router must be a Router instance'

        self._costs = {}
        self._routing_table = {}

        for port in router._ports: # TODO: change to use proper accessor
            link = port.out_link()
            destination = link.destination()
            cost = link.cost()

            self._costs[destination] = cost
            self._routing_table[destination] = port

        # TODO: create set of packets with costs to send to neighbors

        # TODO: wrap packets in events schedule for time zero

    # Overrides Algorithm.next(device)
    def next(self, device):
        """
        Returns the port used to reach the specified device.
        """

        # Checks that device is a Device instance
        if not isinstance(device, Device):
            raise TypeError, 'device must be a Device instance'

        return self._routing_table[device]

    # Overrides Algorithm.update(packet)
    def update(self, packet):
        """
        Updates the routing algorithm using the specified packet.
        Returns True if the cost and routing information was changed
            as a result of the specified packet, and False otherwise.
        """

        # TODO: verify the destination of the specified packet

        changed = False

        next = packet.source() # from reference point of this instance
        next_cost = self._costs[next] # TODO: handle when no cost exists

        costs = packet.datum(_COSTS) # TODO: handle when no data found

        # Iterates through each destination and cost from the packet data
        for (destination, cost) in costs.iteritems():
            overall_cost = cost + next_cost
            current_cost = self._costs.get(destination, -1)

            # Checks whether new or better route found
            if current_cost == -1 or overall_cost < current_cost:
                # Updates cost to destination
                self._costs[destination] = overall_cost

                # Updates routing table to destination
                self._routing_table[destination] = self._routing_table[next]

                changed = True

        return changed
