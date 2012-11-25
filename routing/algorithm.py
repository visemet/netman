class RoutingAlgorithm:
    """
    Base class for routing algorithms.
    """

    def initialize(self, router):
        """
        Initializes the routing algorithm using the specified router.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'RoutingAlgorithm.initialize(router)'

    def next(self, device):
        """
        Returns the port used to reach the specified device.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'RoutingAlgorithm.next(device)'

    def prepare(self, packet):
        """
        Adds routing and cost information to the specified packet.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'RoutingAlgorithm.prepare(packet)'

    def update(self, packet):
        """
        Updates the routing algorithm using the specified packet.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'RoutingAlgorithm.update(packet)'
