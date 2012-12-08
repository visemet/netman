import sys

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

    _EPSILON = 1

    def _find_cost(self, time, dest):
        """
        Computes the cost to reach the specified destination.
        """

        if dest not in self._routing_table:
            return -1

        link = self._routing_table[dest].conn()
        return (link.cost(time) + self._costs[dest])

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

            self._costs[dest] = 0
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
    def prepare(self, time, packet):
        """
        Adds routing and cost information to the specified packet.
        """

        # Checks that packet is a Packet instance
        if not isinstance(packet, Packet):
            raise TypeError, 'packet must be a Packet instance'

        costs = {}

        for dest in self._routing_table:
            costs[dest] = self._find_cost(time, dest)

        packet.datum(BellmanFord._COSTS, costs)
        packet.datum(BellmanFord._TYPE, True)

    # Overrides RoutingAlgorithm.update(packet)
    def update(self, time, packet):
        """
        Updates the routing algorithm using the specified packet.
        Returns True if the cost and routing information was changed
            as a result of the specified packet, and False otherwise.
        """

        # TODO: verify the destination of the specified packet

        changed = False

        next = packet.source() # from reference point of this instance
        next_cost = self._find_cost(time, next)

        costs = packet.datum(BellmanFord._COSTS) # TODO: handle when no data found

        # Iterates through each destination and cost from the packet data
        for (dest, cost) in costs.iteritems():
            if dest == self._router:
                continue

            overall_cost = next_cost + cost
            current_cost = self._find_cost(time, dest)

            # Checks whether new or better route found
            if current_cost == -1 or overall_cost < (current_cost - BellmanFord._EPSILON):
                # Updates cost to destination
                self._costs[dest] = self._costs[next] + cost

                # Updates route to destination
                self._routing_table[dest] = self._routing_table[next]

                changed = True

                print >> sys.stderr, '[%.3f] Router %s choosing route to %s using %s because %s' % (time, self._router, dest, next, packet)

        return changed
