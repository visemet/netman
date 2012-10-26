class RoutingAlgorithm:
    """
    Base class for routing algorithms.
    """

    def initialize(self, router):
        """
        Initializes the routing algorithm using the specified router.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'Algorithm.initialize(router)'

    def next(self, device):
        """
        Returns the port used to reach the specified device.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'Algorithm.next(device)'

    def update(self, packet):
        """
        Updates the routing algorithm using the specified packet.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'Algorithm.update(packet)'
