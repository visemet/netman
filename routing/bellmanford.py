from copy import copy

from algorithm import RoutingAlgorithm
from device import Device
from packet import Packet
from router import Router

class BellmanFord(RoutingAlgorithm):
    """
    Logic for Bellman-Ford algorithm.
    """

    _COSTS = 'costs'
    _TYPE = 'bellman-ford'

    # Overrides RoutingAlgorithm.initialize(router)
    def initialize(self, router):
        """
        Initializes the routing algorithm using the specified router.
        """

        # Checks that router is a Router instance
        if not isinstance(router, Router):
            raise TypeError, 'router must be a Router instance'

        self._router = router

        self._costs = {}
        self._routing_table = {}

        for port in router._ports: # TODO: change to use proper accessor
            link = port.conn()
            dest = link.dest().source()
            cost = link.cost()

            self._costs[dest] = cost
            self._routing_table[dest] = port

    # Overrides RoutingAlgorithm.next(device)
    def next(self, device):
        """
        Returns the port used to reach the specified device.
        """

        # Checks that device is a Device instance
        if not isinstance(device, Device):
            raise TypeError, 'device must be a Device instance'

        return self._routing_table.get(device)

    # Overrides RoutingAlgorithm.prepare(packet)
    def prepare(self, packet):
        """
        Adds routing and cost information to the specified packet.
        """

        # Checks that packet is a Packet instance
        if not isinstance(packet, Packet):
            raise TypeError, 'packet must be a Packet instance'

        packet.datum(BellmanFord._COSTS, copy(self._costs))
        packet.datum(BellmanFord._TYPE, True)

    # Overrides RoutingAlgorithm.update(packet)
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

        costs = packet.datum(BellmanFord._COSTS) # TODO: handle when no data found

        # Iterates through each destination and cost from the packet data
        for (dest, cost) in costs.iteritems():
            if dest == self._router:
                continue

            overall_cost = cost + next_cost
            current_cost = self._costs.get(dest, -1)

            # Checks whether new or better route found
            if current_cost == -1 or overall_cost < current_cost:
                # Updates cost to destination
                self._costs[dest] = overall_cost

                # Updates routing table to destination
                self._routing_table[dest] = self._routing_table[next]

                changed = True

            # Checks whether dynamic cost of known route has increased
            elif (self._routing_table[dest] == self._routing_table[next]
                  and self._routing_table[dest].conn().dest().source() == next
                  and overall_cost > current_cost):

                # Updates cost to destination
                self._costs[dest] = overall_cost

                changed = True

        return changed