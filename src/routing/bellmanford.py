from algorithm import RoutingAlgorithm
from device import Device
from router import Router

class BellmanFord(RoutingAlgorithm):
    """
    """

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
        """

        raise NotImplementedError, 'BellmanFord.update(packet)'
