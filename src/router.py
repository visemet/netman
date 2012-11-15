import sys

from conn import Port
from device import Device
from event import Event
from flow import Flow
from routing.algorithm import RoutingAlgorithm
from packet import Packet

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

        self._ports = []
        self._flows = {}

    def enable(self, port):
        """
        Adds the specified port to the set of ports.
        """

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must be a Port instance'

        self._ports.append(port)

    def neighbors(self):
        """
        Returns the list of directly connected routers.
        """

        return [port.conn().dest().source() for port in self._ports]

    # Overrides Device.initialize()
    def initialize(self):
        """
        Initializes the router.
        """

        events = []

        # Creates a flow for each neighbor of the router
        for dest in self.neighbors():
            flow = Flow(None) # TODO: choose congestion algorithm
            flow.start(0)
            flow.dest(dest)
            self._flows[dest] = flow

        # Initializes the routing algorithm
        packets = self._algorithm.initialize(self)

        # Iterates through each flow
        for flow in self._flows.values():
            # Checks that flow can and wants to send data
            if flow.is_able() and flow.has_data():
                # Gets packet for corresponding destination
                packet = packets[flow.dest()]
                # Attaches a unique identifier (per flow) to the packet
                packet.seq(flow.next_seq())

                dest = packet.dest()
                port = self._algorithm.next(dest)

                # Checks that destination is reachable
                if port is None:
                    continue

                # Creates an event for the starting time of the flow
                event = Event()
                event.scheduled(flow.start())
                event.action(Event._SEND)
                event.packet(packet)

                events.append(event)

        return events

    # Overrides Device.process(event)
    def process(self, event):
        """
        Processes the specified event.
        """

        events = []

        time = event.scheduled()
        port = event.port()
        action = event.action()

        if action == Event._RECEIVE:
            # Processes all received packets
            while port.incoming():
                packet = port.incoming().popleft() # append right, pop left

                print >> sys.stderr, 'Router %s received packet %s' % (self, packet)
                # exit()

                # TODO: handle hello packet
                if packet.has_datum(self._algorithm._TYPE):
                    update_ports = self._algorithm.update(packet)

                    if update_ports is not None:
                        for update_port in update_ports:
                            update_event = Event()
                            update_event.scheduled(time)
                            update_event.port(port)
                            update_event.action(Event._SEND)

                            events.append(update_event)

                    # TODO: send acknowledgment to packet source

                # TODO: otherwise, forward packet onward
                #       (place in outgoing queue)
                else:
                    port.outgoing().append(packet) # append right, pop left

                    # TODO: create send event at current time

        elif action == Event._SEND:
            # Processes at most one outgoing packet
            if port.outgoing():
                # TODO: ensure window size is greater than number of outstanding packets

                packet = port.outgoing().popleft() # append right, pop left

                print >> sys.stderr, 'Router %s sent packet %s' % (self, packet)

                # TODO: forward packet onward
                #       (place in incoming queue of next hop)
                link = port.conn()
                prop_delay = link.delay()
                dest = link.dest()

                dest.incoming().append(packet) # append right, pop left

                spawned_event = Event()
                spawned_event.scheduled(time + prop_delay)
                spawned_event.port(dest)
                spawned_event.action(Event._RECEIVE)
                spawned_event.packet(packet)

                events.append(spawned_event)

                # TODO: create send event at tranmission delay later
                # trans_delay = packet.size() / link.rate()

        return events
