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

    def update(self, packet):
        """
        Updates the routing algorithm using the specified packet.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'Algorithm.update(packet)'
