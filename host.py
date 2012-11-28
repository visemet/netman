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

        flow = self._flows[dest]
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

                if flow is not None:
                    flow.analyze(event)

                    if flow.is_able() and flow.has_data():

                        # Checks that destination is reachable
                        if self._port is not None:
                            next_packet = self._create_packet(self, dest)

                            # Attaches a unique identifier (per flow) to the packet
                            flow.prepare(next_packet)

                            self._port.outgoing().append(next_packet) # append right, pop left

                            send_event = self._create_event(time, self._port, Event._SEND, next_packet)

                            events.append(send_event)

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
            pass

            # TODO: notify link that packet was dropped

        # Otherwise, forwards packet onward
        else:
            queue.append(packet) # append right, pop left

            # TODO: notify link that packet was sent

            receive_event = self._create_event(time + prop_delay, dest, Event._RECEIVE, packet)
            events.append(receive_event)

        if packet.source() == self:
            # Updates packet statistics of flow
            flow = self._flows.get(packet.dest())

            if flow is not None:
                flow.analyze(event)

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
        port = event.port()
        action = event.action()

        if action == Event._CREATE:
            events.extend(self._handle_create(event))

        elif action == Event._RECEIVE:
            # Processes all received packets
            if port.incoming():
                # Pops the packet off the head of the queue
                packet = port.incoming().popleft() # append right, pop left
                event.packet(packet)

                print >> sys.stderr, '[%.3f] Host %s received packet %s' % (time, self, packet)

                events.extend(self._handle_receive(event))

        elif action == Event._SEND:
            # Processes at most one outgoing packet
            if port.outgoing():
                # TODO: ensure window size is greater than number of outstanding packets

                packet = port.outgoing().popleft() # append right, pop left
                event.packet(packet)

                print >> sys.stderr, '[%.3f] Host %s sent packet %s' % (time, self, packet)

                events.extend(self._handle_send(event))

        return events