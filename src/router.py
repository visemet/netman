from device import Device

class Router(Device):
    """
    """

    def __init__(self, algorithm):
        """
        Creates a Router instance with the specified algorithm.
        """

        # TODO: Check algorithm isinstance(routing.algorithm.Algorithm)
        self._algorithm = algorithm

        self._ports = set()
        self._routing_table = dict()

    def enable(self, port):
        """
        Adds the specified port to the set of ports.
        """

        # TODO: Check port isinstance(port.Port)
        self._port.add(port)

    def neighbors(self):
        """
        Returns the directly connected routers as a set.
        """

        raise NotImplementedError('Router.neighbors()')

    # Overrides Device.initialize()
    def initialize(self):
        """
        Initializes the router.
        """

        raise NotImplementedError('Router.initialize()')

    # Overrides Device.send(packet)
    def send(self, packet):
        """
        Sends the specified packet.
        """

        raise NotImplementedError('Router.send(packet)');

    # Overrides Device.process(event)
    def process(self, event):
        """
        Processes the specified event.
        """
        
        raise NotImplementedError('Router.process(event)')   
