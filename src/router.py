import sys

from device import Device
from event import Event
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

    def __repr__(self):
        """
        """

        return self.__str__()

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

        time = event.schedule()
        port = event.port()

        # Processes all received packets
        while port.in_queue():
            packet = port.in_queue().popleft() # append right, pop left

            print >> sys.stderr, 'Router %s received packet %s' % (self, packet)
            # exit()

            # TODO: handle hello packet
            if packet.has(self._algorithm._TYPE):
                update_ports = self._algorithm.update(packet)

                if update_ports is not None:
                    for update_port in update_ports:
                        update_event = Event(time, port)
                        events.append(update_event)

            # TODO: otherwise, forward packet onward
            #       (place in outgoing queue)
            else:
                port.out_queue().append(packet) # append right, pop left

        # Processes at most one outgoing packet
        if port.out_queue():
            # TODO: ensure window size is greater than number of outstanding packets

            packet = port.out_queue().popleft() # append right, pop left

            print >> sys.stderr, 'Router %s sent packet %s' % (self, packet)

            # TODO: forward packet onward
            #       (place in incoming queue of next hop)
            link = port.out_link()
            delay = link.delay()
            destination = link.destination()

            destination.in_queue().append(packet) # append right, pop left

            spawned_event = Event(time + delay, destination)
            events.append(spawned_event)

        return events
