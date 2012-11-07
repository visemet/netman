from device import Device
from port import Port
from routing.algorithm import RoutingAlgorithm

class Router(Device):
    """
    Builder for Router instances.
    """

    def __init__(self, algorithm, identifier):
        """
        Creates a Router instance with the specified algorithm and the
        specified identifier.
        """

        Device.__init__(self, identifier)

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

        return set(port.out_link().destination().device() for port in self._ports)

    # Overrides Device.initialize()
    def initialize(self):
        """
        Initializes the router.
        """

        events = []

        ports = self._algorithm.initialize(self)
        for port in ports:
            event = Event(0, port)
            events.append(event)

        return events

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

        events = []

        port = event.port()

        # Processes all received packets
        while port.in_queue():
            packet = port.in_queue().popleft() # append right, pop left

            # TODO: handle hello packet
            events.extend(self._algorithm.update(packet))

            # TODO: otherwise, forward packet onward
            #       (place in outgoing queue)

        # Processes at most one outgoing packet
        if port.out_queue():
            # TODO: ensure window size is greater than number of outstanding packets

            packet = port.out_queue().popleft() # append right, pop left

            # TODO: forward packet onward
            #       (place in incoming queue of next hop)

        return events
