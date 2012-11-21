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
        self._algorithm.initialize(self)

        for (dest, flow) in self._flows.iteritems():
            packet = Packet()
            packet.source(self)
            packet.dest(dest)

            port = self._algorithm.next(dest)

            # Checks that destination is reachable
            if port is None:
                continue

            # Creates an event for the starting time of the flow
            event = Event()
            event.scheduled(flow.start())
            event.port(port)
            event.action(Event._CREATE)
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

        if action == Event._CREATE:
            packet = event.packet()
            dest = packet.dest()

            flow = self._flows[dest]
            if flow.is_able() and flow.has_data(): # always true
                next_port = self._algorithm.next(dest)

                if next_port is not None:
                    # Attaches a unique identifier (per flow) to the packet
                    packet.seq(flow.next_seq())

                    # Adds routing and cost information to the packet
                    self._algorithm.prepare(packet)

                    next_port.outgoing().append(packet) # append right, pop left

                    routing_event = Event()
                    routing_event.scheduled(time)
                    routing_event.port(next_port)
                    routing_event.action(Event._SEND)
                    # routing_event.packet(packet)

                    events.append(routing_event)

        elif action == Event._RECEIVE:
            # Processes all received packets
            if port.incoming():
                # Pops the packet off the head of the queue
                packet = port.incoming().popleft() # append right, pop left

                print >> sys.stderr, '[%.3f] Router %s received packet %s' % (time, self, packet)

                # Checks that packet was destined for this router
                if packet.dest() == self:
                    dest = packet.source()
                    event.packet(packet)

                    # TODO: handle acknowledgment received
                    if packet.has_datum(Packet._ACK):
                        # Updates packet statistics of flow
                        flow = self._flows.get(dest)

                        if flow is not None:
                            flow.analyze(event)
                            # print >> sys.stderr, 'Router %s has received %d packets at %s%s' % (self, len(flow._tracker._times_received), flow.dest(), flow._tracker._times_received)
                    else:
                        changed = False

                        # Updates the routing and cost information if necessary
                        if packet.has_datum(self._algorithm._TYPE):
                            changed = self._algorithm.update(packet)

                        next_port = self._algorithm.next(dest)

                        # Sends an acknowledgment to the source
                        ack = Packet()
                        ack.seq(packet.seq())
                        ack.source(self)
                        ack.dest(dest)
                        ack.datum(Packet._ACK, True)

                        next_port.outgoing().append(ack) # append right, pop left

                        ack_event = Event()
                        ack_event.scheduled(time)
                        ack_event.port(next_port)
                        ack_event.action(Event._SEND)
                        # ack_event.packet(ack)

                        events.append(ack_event)

                        # Checks that routing or cost information has changed
                        if changed:
                            # Handles a hello packet
                            for (dest, flow) in self._flows.iteritems():
                                update_packet = Packet()
                                update_packet.source(self)
                                update_packet.dest(dest)

                                self._algorithm.prepare(update_packet)

                                next_port = self._algorithm.next(dest)

                                # Checks that destination is reachable
                                if next_port is not None:
                                    if flow.is_able() and flow.has_data():
                                        # Attaches a unique identifier (per flow) to the packet
                                        update_packet.seq(flow.next_seq())

                                        next_port.outgoing().append(update_packet) # append right, pop left

                                        update_event = Event()
                                        update_event.scheduled(time)
                                        update_event.port(next_port)
                                        update_event.action(Event._SEND)
                                        # update_event.packet(update_packet)

                                        events.append(update_event)

                # Otherwise, forward packet onward
                else:
                    dest = packet.dest()
                    next_port = self._algorithm.next(dest)

                    # Checks that destination is reachable
                    if next_port is not None:
                        next_port.outgoing().append(packet) # append right, pop left

                        # TODO: create send event at current time
                        next_event = Event()
                        next_event.scheduled(time)
                        next_event.port(next_port)
                        next_event.action(Event._SEND)
                        next_event.packet(packet)

                        events.append(next_event)

        elif action == Event._SEND:
            # Processes at most one outgoing packet
            if port.outgoing():
                # TODO: ensure window size is greater than number of outstanding packets

                packet = port.outgoing().popleft() # append right, pop left
                event.packet(packet)

                print >> sys.stderr, '[%.3f] Router %s sent packet %s' % (time, self, packet)

                # TODO: forward packet onward
                #       (place in incoming queue of next hop)
                link = port.conn()
                prop_delay = link.delay()
                dest = link.dest()

                dest.incoming().append(packet) # append right, pop left

                if packet.source() == self:
                    # Updates packet statistics of flow
                    flow = self._flows.get(packet.dest())

                    if flow is not None:
                        flow.analyze(event)
                        # print >> sys.stderr, 'Router %s has sent %d packets at %s%s' % (self, len(flow._tracker._times_sent), flow.dest(), flow._tracker._times_sent)


                # TODO: create timeout event at timeout length later

                spawned_event = Event()
                spawned_event.scheduled(time + prop_delay)
                spawned_event.port(dest)
                spawned_event.action(Event._RECEIVE)
                # spawned_event.packet(packet)

                events.append(spawned_event)

                # TODO: create send event at tranmission delay later
                # trans_delay = packet.size() / link.rate()

        return events
