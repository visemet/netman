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

    def _create_packet(self, source, dest):
        """
        Creates a packet instance with the specified source and
        destination devices.
        """

        packet = Packet()
        packet.source(source)
        packet.dest(dest)
        packet.size(Packet._DATA_SIZE)

        return packet

    def _create_ack(self, packet):
        """
        Creates an acknowledgment in reponse to the specified packet.
        """

        num = packet.seq()
        source = packet.dest()
        dest = packet.source()

        ack = self._create_packet(source, dest)

        ack.seq(num)
        ack.size(Packet._ACK_SIZE)
        ack.datum(Packet._ACK, True)

        return ack

    def _create_event(self, time, port, action, packet):
        """
        Creates an Event instance with the specified time, port, action
        and packet.
        """

        event = Event()
        event.scheduled(time)
        event.port(port)
        event.action(action)
        event.packet(packet)

        return event

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
            packet = self._create_packet(self, dest)

            port = self._algorithm.next(dest)

            # Checks that destination is reachable
            if port is None:
                continue

            # Creates an event for the starting time of the flow
            event = self._create_event(flow.start(), port, Event._CREATE, packet)

            events.append(event)

        return events

    def _handle_create(self, event):
        """
        Handles create events.
        """

        events = []

        time = event.scheduled()
        packet = event.packet()

        dest = packet.dest()

        flow = self._flows[dest]
        if flow.is_able() and flow.has_data(): # always true
            next_port = self._algorithm.next(dest)

            if next_port is not None:
                # Attaches a unique identifier (per flow) to the packet
                flow.prepare(packet)

                # Adds routing and cost information to the packet
                self._algorithm.prepare(packet)

                next_port.outgoing().append(packet) # append right, pop left

                routing_event = self._create_event(time, next_port, Event._SEND, packet)

                events.append(routing_event)

        return events

    def _handle_receive(self, event):
        """
        Handles receive events.
        """

        events = []

        time = event.scheduled()
        packet = event.packet()

        # Checks that packet was destined for this router
        if packet.dest() == self:
            dest = packet.source()

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
                ack = self._create_ack(packet)

                next_port.outgoing().append(ack) # append right, pop left

                ack_event = self._create_event(time, next_port, Event._SEND, ack)

                events.append(ack_event)

                # Checks that routing or cost information has changed
                if changed:
                    # Handles a hello packet
                    for (dest, flow) in self._flows.iteritems():
                        update_packet = self._create_packet(self, dest)

                        self._algorithm.prepare(update_packet)

                        next_port = self._algorithm.next(dest)

                        # Checks that destination is reachable
                        if next_port is not None:
                            if flow.is_able() and flow.has_data():
                                # Attaches a unique identifier (per flow) to the packet
                                flow.prepare(update_packet)

                                next_port.outgoing().append(update_packet) # append right, pop left

                                update_event = self._create_event(time, next_port, Event._SEND, update_packet)

                                events.append(update_event)

        # Otherwise, forward packet onward
        else:
            dest = packet.dest()
            next_port = self._algorithm.next(dest)

            # Checks that destination is reachable
            if next_port is not None:
                next_port.outgoing().append(packet) # append right, pop left

                # Creates a send event at the current time
                next_event = self._create_event(time, next_port, Event._SEND, packet)

                events.append(next_event)

        return events

    def _handle_send(self, event):
        """
        Handles send events.
        """

        events = []

        time = event.scheduled()
        port = event.port()
        packet = event.packet()

        # TODO: forward packet onward
        #       (place in incoming queue of next hop)
        link = port.conn()
        prop_delay = link.delay()
        dest = link.dest()

        queue = dest.incoming()
        if queue.has_space(packet):
            queue.append(packet) # append right, pop left

            spawned_event = self._create_event(time + prop_delay, dest, Event._RECEIVE, packet)
            events.append(spawned_event)

        if packet.source() == self:
            # Updates packet statistics of flow
            flow = self._flows.get(packet.dest())

            if flow is not None:
                flow.analyze(event)
                # print >> sys.stderr, 'Router %s has sent %d packets at %s%s' % (self, len(flow._tracker._times_sent), flow.dest(), flow._tracker._times_sent)


        # TODO: create timeout event at timeout length later

        # TODO: create send event at tranmission delay later
        # trans_delay = packet.size() / link.rate()

        return events

    # Overrides Device.process(event)
    def process(self, event):
        """
        Processes the specified event.
        """

        events = []

        time = event.scheduled()
        action = event.action()
        port = event.port()

        if action == Event._CREATE:
            events.extend(self._handle_create(event))

        elif action == Event._RECEIVE:
            # Processes all received packets
            if port.incoming():
                # Pops the packet off the head of the queue
                packet = port.incoming().popleft() # append right, pop left
                event.packet(packet)

                print >> sys.stderr, '[%.3f] Router %s received packet %s' % (time, self, packet)

                events.extend(self._handle_receive(event))

        elif action == Event._SEND:
            # Processes at most one outgoing packet
            if port.outgoing():
                # TODO: ensure window size is greater than number of outstanding packets

                packet = port.outgoing().popleft() # append right, pop left
                event.packet(packet)

                print >> sys.stderr, '[%.3f] Router %s sent packet %s' % (time, self, packet)

                events.extend(self._handle_send(event))

        return events
