from device import Device
from port import Port
from routing.algorithm import RoutingAlgorithm

class Router(Device):
    """
    """

    def __init__(self, algorithm):
        """
        Creates a Router instance with the specified algorithm.
        """

        # Checks that algorithm is a RoutingAlgorithm instance
        if not isinstance(algorithm, RoutingAlgorithm):
            raise TypeError, 'algorithm must be a RoutingAlgorithm instance'

        self._algorithm = algorithm

        self._ports = set()

    def enable(self, port):
        """
        Adds the specified port to the set of ports.
        """

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must be a Port instance'

        self._ports.add(port)

    def neighbors(self):
        """
        Returns the directly connected routers as a set.
        """

        return set(port.out_link().destination() for port in self._ports)

    # Overrides Device.initialize()
    def initialize(self):
        """
        Initializes the router.
        """

        self._algorithm.initialize(self)

    # Overrides Device.send(packet)
    def send(self, packet):
        """
        Sends the specified packet.
        """

        raise NotImplementedError, 'Router.send(packet)'

    # Overrides Device.process(event)
    def process(self, event):
        """
        Processes the specified event.
        """
        
        raise NotImplementedError, 'Router.process(event)'
