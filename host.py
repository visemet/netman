import sys

from conn import Port
from device import Device
from event import Event
from flow import Flow
from packet import Packet
from router import Router

class Host(Device):
    """
    Builder for Host instances.
    """

    def __init__(self, identifier):
        """
        Creates a Host instance with the specified port and the
        specified identifier.
        """

        Device.__init__(self, identifier)

        self._flows = {}

    def get_flows(self):
        return self._flows

    #caution: should not be called until after host has been completely set up
    # (i.e. only used in simulation.finalize()
    def get_ports(self):
        return self._port

    def enable(self, port):
        """
        Replaces the port with the specified value.
        """

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must be a Port instance'

        self._port = port

    def connect(self, flow):
        """
        Adds the specified flow to the set of flows.
        """

        # Checks that flow is a Flow instance
        if not isinstance(flow, Flow):
            raise TypeError, 'flow must be a Flow instance'

        self._flows[flow.dest()] = flow

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
        Initializes the host.
        """

        events = []

        # Iterates through each flow
        for (dest, flow) in self._flows.iteritems():
            # Creates a packet to send
            packet = self._create_packet(self, dest)

            # Checks that destination is reachable
            if self._port is None:
                continue

            # Creates an event for the starting time of the flow
            event = self._create_event(flow.start(), self._port, Event._CREATE, packet)

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

        flow = self._flows.get(dest)

        if flow is not None:

            if flow.is_able() and flow.has_data():

                # Checks that destination is reachable
                if self._port is not None:
                    # Attaches a unique identifier (per flow) to the packet
                    flow.prepare(packet)

                    self._port.outgoing().append(packet) # append right, pop left

                    send_event = self._create_event(time, self._port, Event._SEND, packet)

                    events.append(send_event)


        return events

    def _handle_receive(self, event):
        """
        Handles receive events.
        """

        events = []

        time = event.scheduled()
        packet = event.packet()

        # Checks that packet was destined for this host
        if packet.dest() == self:
            dest = packet.source()

            # Handles acknowledgment received
            if packet.has_datum(Packet._ACK):
                # Updates packet statistics of the flow
                flow = self._flows.get(dest)

                should_create = False

                if flow is not None:
                    should_create = not flow.is_able()

                    flow.analyze(event, None)

                # Only create a create event if previously unable to send
                if should_create:
                    next_packet = self._create_packet(self, dest)

                    create_event = self._create_event(time, self._port, Event._CREATE, next_packet)

                    events.append(create_event)
                    print >> sys.stderr, "should create" + str( time)

            # Otherwise, creates an acknowledgment packet
            else:
                ack = self._create_ack(packet)

                self._port.outgoing().append(ack) # append right, pop left

                ack_event = self._create_event(time, self._port, Event._SEND, ack)

                events.append(ack_event)

        return events

    def _handle_send(self, event):
        """
        Handles send events.
        """

        events = []

        time = event.scheduled()
        port = event.port()
        packet = event.packet()

        link = port.conn()
        prop_delay = link.delay()
        dest = link.dest()

        queue = dest.incoming()

        # Checks if the room for packet on receiving end
        if not queue.has_space(packet):
            # Notifies the link that a packet was dropped
            link.record_packet_loss(time + prop_delay)

        # Otherwise, forwards packet onward
        else:
            queue.append(packet) # append right, pop left

            # Notifies the link that a packet was sent


            receive_event = self._create_event(time + prop_delay, dest, Event._RECEIVE, packet)
            events.append(receive_event)

        should_create = True
        if packet.source() == self:
            # Updates packet statistics of flow
            flow = self._flows.get(packet.dest())

            if flow is not None:
                flow.analyze(event, link)
                should_create = flow.is_able()

        if event.action() == Event._SEND and not packet.has_datum(Packet._ACK):
            link.record_sent(time, packet.size())
            #rate = link.throughput(
            #    link.getTracker().get_previous_linkrate_point(), time)
            #link.getTracker().record_linkrate(time, rate)


        # Creates the next packet to send
        next_packet = self._create_packet(self, dest.source())

        # Creates a timeout event for a timeout length later
        timeout_event = self._create_event(time + link.timeout(), self._port, Event._TIMEOUT, next_packet)
        events.append(timeout_event)

        # Creates a create event for a tranmission delay later
        trans_delay = float(packet.size()) / float(link.rate())

        if should_create:
            create_event = self._create_event(time + trans_delay, self._port, Event._CREATE, next_packet)
            events.append(create_event)

        return events

    def _handle_timeout(self, event):
        """
        Handles timeout events.
        """

        events = []

        packet = event.packet()

        # Updates packet statistics of flow
        flow = self._flows.get(packet.dest())

        if flow is not None:
            flow.analyze(event, None)

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
        link = port.conn()


        if action == Event._CREATE:
            events.extend(self._handle_create(event))

        elif action == Event._RECEIVE:
            link.dest().conn().record_buffer_size(time, len(port.incoming()))
            # Processes an incoming packet
            if port.incoming():
                # Pops the packet off the head of the queue
                packet = port.incoming().popleft() # append right, pop left
                event.packet(packet)

                print >> sys.stderr, '[%.3f] Host %s received packet %s' % (time, self, packet)

                events.extend(self._handle_receive(event))
            link.dest().conn().record_buffer_size(time, len(port.incoming()))

        elif action == Event._SEND:
            link.record_buffer_size(time, len(port.conn().dest().incoming()))
            # Processes an outgoing packet
            if port.outgoing():

                # TODO: ensure window size is greater than number of outstanding packets

                # Pops the packet off the head of the queue
                packet = port.outgoing().popleft() # append right, pop left
                event.packet(packet)

                print >> sys.stderr, '[%.3f] Host %s sent packet %s' % (time, self, packet)

                events.extend(self._handle_send(event))
            link.record_buffer_size(time, len(port.conn().dest().incoming()))

        elif action == Event._TIMEOUT:
            events.extend(self._handle_timeout(event))

        return events
