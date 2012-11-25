from algorithm import RoutingAlgorithm
from device import Device
from router import Router

class Static(RoutingAlgorithm):
    """
    """

    # Overrides Algorithm.initialize(router)
    def initialize(self, router):
        """
        Initializes the routing algorithm using the specified router.
        Implemented in each subclass.
        """

        # Checks that router is a Router instance
        if not isinstance(router, Router):
            raise TypeError, 'router must be a Router instance'

        self._routing_table = dict([(port.out_link().destination(), port)
                                    for port in router._ports])

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
        Implemented in each subclass.
        """

        raise NotImplementedError, 'Static.update(packet)'
