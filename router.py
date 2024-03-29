import sys

from congestion.aimd import AIMD
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

    _UPDATE_EVERY = 4000

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

        self._changed = {}

        self._most_recent = {}
        self._next_update = 0

        self._should_update = False

    def get_ports(self): 
        return self._ports
        
    def get_flows(self):
        return self._flows
    
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

        ack.set_create_time(packet.get_create_time())
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
            if not isinstance(dest, Router):
                continue

            congestion = AIMD()

            flow = Flow(congestion)
            flow.start(0)
            flow.dest(dest)

            congestion.initialize(flow)

            self._flows[dest] = flow
            self._changed[dest] = False

        # Initializes the routing algorithm
        self._algorithm.initialize(self)

        for (dest, flow) in self._flows.iteritems():
            packet = self._create_packet(self, dest)

            packet.set_create_time(flow.start())

            port = self._algorithm.next(dest)

            # Checks that destination is reachable
            if port is None:
                continue

            # Creates an event for the starting time of the flow
            create_event = self._create_event(flow.start(), port, Event._CREATE, packet)
            events.append(create_event)

        self._next_update += Router._UPDATE_EVERY

        return events

    def _schedule(self, time, packet, link):
        """
        Attempts to schedule the specified packet to send through the
        specified link at the specified time.
        """

        next_time = max(self._most_recent.get(link, time), time)

        trans_delay = float(packet.size()) / float(link.rate())
        self._most_recent[link] = next_time + trans_delay

        return next_time

    def _handle_create(self, event):
        """
        Handles create events.
        """

        events = []

        time = event.scheduled()
        packet = event.packet()

        dest = packet.dest()

        next_port = self._algorithm.next(dest)
        if next_port is None:
            # TODO: handle by buffering the packet?
            raise ValueError, 'port must be specified'

        flow = self._flows.get(dest)

        if flow is not None and (flow.is_able() or True) and flow.has_data():
            # Attaches a unique identifier (per flow) to the packet
            flow.prepare(packet)

            # Adds routing and cost information to the packet
            self._algorithm.prepare(time, packet)

            next_port.outgoing().append(packet) # append right, pop left

            link = next_port.conn()

            link.record_packet_entry(packet, time)
            send_time = self._schedule(time, packet, link)

            routing_event = self._create_event(send_time, next_port, Event._SEND, packet)
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
                    flow.analyze(event, None)
                    # print 'after analyze', self, flow.window()
                    # print >> sys.stderr, 'Router %s has received %d packets at %s%s' % (self, len(flow._tracker._times_received), flow.dest(), flow._tracker._times_received)

                    next_time = time

                    # if not self._changed[dest]:
                    if not self._should_update:
                        next_time = self._next_update
                        self._next_update += Router._UPDATE_EVERY

                    self._changed[dest] = False
                    self._should_update = False

                    # Handles a hello packet
                    for (dest, flow) in self._flows.iteritems():
                        next_packet = self._create_packet(self, dest)
                        next_packet.set_create_time(time)

                        next_port = self._algorithm.next(dest)

                        # Creates a create event for the current time
                        create_event = self._create_event(next_time, next_port, Event._CREATE, next_packet)
                        events.append(create_event)

            else:
                changed = False

                # Updates the routing and cost information if necessary
                if packet.has_datum(self._algorithm._TYPE):
                    changed = self._algorithm.update(time, packet)

                next_port = self._algorithm.next(dest)

                # Sends an acknowledgment to the source
                ack = self._create_ack(packet)

                next_port.outgoing().append(ack) # append right, pop left

                link = next_port.conn()

                link.record_packet_entry(ack, time)
                send_time = self._schedule(time, ack, link)

                ack_event = self._create_event(send_time, next_port, Event._SEND, ack)
                events.append(ack_event)

                self._changed[dest] = changed
                self._should_update |= changed

        # Otherwise, forward packet onward
        else:
            dest = packet.dest()
            next_port = self._algorithm.next(dest)

            # Checks that destination is reachable
            if next_port is not None:
                next_port.outgoing().append(packet) # append right, pop left

                link = next_port.conn()

                link.record_packet_entry(packet, time)
                send_time = self._schedule(time, packet, link)

                # Creates a send event at the current time
                next_event = self._create_event(send_time, next_port, Event._SEND, packet)
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
        
        else: # no room, record the dropped packet
            link.record_packet_loss(time+prop_delay)

        if packet.source() == self:
            # Updates packet statistics of flow
            flow = self._flows.get(packet.dest())

            if flow is not None:
                flow.analyze(event, link)
                # print >> sys.stderr, 'Router %s has sent %d packets at %s%s' % (self, len(flow._tracker._times_sent), flow.dest(), flow._tracker._times_sent)

        if event.action() == Event._SEND and not packet.has_datum(Packet._ACK):
            link.record_sent(time, packet.size())

        # TODO: create timeout event at timeout length later

        # TODO: create send event at tranmission delay later
        trans_delay = float(packet.size()) / float(link.rate())

        return events

    def _handle_timeout(self, event):
        """
        Handles timeout events.
        """

        events = []

        time = event.scheduled()
        port = event.port()
        packet = event.packet()

        dest = packet.dest()

        # Updates packet statistics of flow
        flow = self._flows.get(dest)

        if flow is not None:
            flow.analyze(event, None)

        # TODO: necessary to create send event at current time?

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
        link = port.conn()

        if action == Event._CREATE:
            events.extend(self._handle_create(event))

        elif action == Event._RECEIVE:
            link.dest().conn().record_buffer_size(time, len(port.incoming()))

            # Processes all received packets
            if port.incoming():
                # Pops the packet off the head of the queue
                packet = port.incoming().popleft() # append right, pop left
                event.packet(packet)

                print >> sys.stderr, '[%.3f] Router %s received packet %s' % (time, self, packet)

                events.extend(self._handle_receive(event))

            link.dest().conn().record_buffer_size(time, len(port.incoming()))

        elif action == Event._SEND:
            link.record_buffer_size(time, len(port.conn().dest().incoming()))

            # Processes at most one outgoing packet
            if port.outgoing():
                # Pops the packet off the head of the queue
                packet = port.outgoing().popleft() # append right, pop left
                event.packet(packet)

                link = port.conn()
                dest = link.dest().source()

                # Updates the queueing delay when a packet is sent
                link.update_queueing_delay(packet, time)

                print >> sys.stderr, '[%.3f] Router %s sent packet %s' % (time, self, packet)

                events.extend(self._handle_send(event))

            link.record_buffer_size(time, len(port.conn().dest().incoming()))

        elif action == Event._TIMEOUT:
            events.extend(self._handle_timeout(event))

        return events
