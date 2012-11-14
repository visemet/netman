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

    def _notify(self):
        """
        Adds packets containing the cost information to the outgoing
        buffers of each port.
        """

        source = self._router

        # TODO: get neighbors of router and create packets to those destination
        #       then use routing table to decide the outgoing port

        for port in source._ports: # TODO: change to use proper accessor
            link = port.conn()
            dest = link.dest().source()

            packet = Packet()
            packet.source(source)
            packet.dest(dest)
            packet.datum(BellmanFord._COSTS, copy(self._costs))
            packet.datum(BellmanFord._TYPE, True)

            # TODO: handle no space in outgoing buffer
            port.outgoing().append(packet) # append right, pop left

        return source._ports

    # Overrides Algorithm.initialize(router)
    def initialize(self, router):
        """
        Initializes the routing algorithm using the specified router.
        """

        # Checks that router is a Router instance
        if not isinstance(router, Router):
            raise TypeError, 'router must be a Router instance'

        self._router = router

        self._costs = {}
        # self._costs = {self._router: 0}
        self._routing_table = {}
        # self._routing_table = {self._router: None}

        for port in router._ports: # TODO: change to use proper accessor
            link = port.conn()
            dest = link.dest().source()
            cost = link.cost()

            self._costs[dest] = cost
            self._routing_table[dest] = port

        # Create set of packets with costs to send to neighbors
        return self._notify()

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

        if changed:
            return self._notify()
