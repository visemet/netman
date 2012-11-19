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

    # Overrides Device.initialize()
    def initialize(self):
        """
        Initializes the host.
        """

        events = []

        # Iterates through each flow
        for (dest, flow) in self._flows.iteritems():
            # Creates a packet to send
            packet = Packet()
            packet.source(self)
            packet.dest(dest)

            # Checks that destination is reachable
            if self._port is None:
                continue

            # Creates an event for the starting time of the flow
            event = Event()
            event.scheduled(flow.start())
            event.port(self._port)
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
                if self._port is not None:
                    # Attaches a unique identifier (per flow) to the packet
                    packet.seq(flow.next_seq())

                    self._port.outgoing().append(packet) # append right, pop left

                    routing_event = Event()
                    routing_event.scheduled(time)
                    routing_event.port(self._port)
                    routing_event.action(Event._SEND)
                    routing_event.packet(packet)

                    events.append(routing_event)

        elif action == Event._RECEIVE:
            # Processes all received packets
            while port.incoming():
                packet = port.incoming().popleft() # append right, pop left

                print >> sys.stderr, 'Host %s received packet %s' % (self, packet)

                # Checks that packet was destined for this host
                if packet.dest() == self:
                    # TODO: handle acknowledgment received
                    if packet.has_datum(Packet._ACK):
                        # TODO: have flow analyze acknowledgment received

                        dest = packet.source()

                        flow = self._flows[dest]
                        if flow.is_able() and flow.has_data(): # always true
                            if self._port is not None:
                                next_packet = Packet()
                                next_packet.source(self)
                                next_packet.dest(dest)

                                # Attaches a unique identifier (per flow) to the packet
                                next_packet.seq(flow.next_seq())

                                self._port.outgoing().append(next_packet) # append right, pop left

                                next_event = Event()
                                next_event.scheduled(time)
                                next_event.port(self._port)
                                next_event.action(Event._SEND)
                                next_event.packet(next_packet)

                                events.append(next_event)

                    # TODO: otherwise, create acknowledgment packet
                    #       (place in outgoing queue)
                    else:
                        dest = packet.source()

                        ack = Packet()
                        ack.source(self)
                        ack.dest(dest)
                        ack.datum(Packet._ACK, True)

                        # Sets the unique identifier (per flow) for acknowledgment as packet received
                        ack.seq(packet.seq())

                        self._port.outgoing().append(ack) # append right, pop left

                        ack_event = Event()
                        ack_event.scheduled(time)
                        ack_event.port(self._port)
                        ack_event.action(Event._SEND)
                        ack_event.packet(ack)

                        events.append(ack_event)
                        

        elif action == Event._SEND:
            # Processes at most one outgoing packet
            if port.outgoing():
                # TODO: ensure window size is greater than number of outstanding packets

                packet = port.outgoing().popleft() # append right, pop left

                # TODO: notify flow that packet has been sent

                print >> sys.stderr, 'Host %s sent packet %s' % (self, packet)

                # TODO: forward packet onward
                #       (place in incoming queue of next hop)
                link = port.conn()
                prop_delay = link.delay()
                dest = link.dest()

                # TODO: determine if packet "will be" lost

                dest.incoming().append(packet) # append right, pop left

                # TODO: notify link that packet sent, and potentially lost at a future time

                # TODO: create timeout event at timeout length later

                spawned_event = Event()
                spawned_event.scheduled(time + prop_delay)
                spawned_event.port(dest)
                spawned_event.action(Event._RECEIVE)
                spawned_event.packet(packet)

                events.append(spawned_event)

                # TODO: create send event at tranmission delay later
                # trans_delay = packet.size() / link.rate()

        return events
