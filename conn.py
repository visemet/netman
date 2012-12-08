from math import sqrt

from buffer import Buffer
from device import Device
from trackers.link import LinkTracker

class Link:
    """
    Builder for Link instances.
    """

    _STATIC = 1
    _DYNAMIC = 1

    _WINDOW = 4000

    def __init__(self):
        """
        Creates a Link instance.
        """
        self._tracker = LinkTracker()

    def __repr__(self):
        """
        Defines the string representation for a Link instance.
        """

        return ('Link['
                'dest=%s'
                ']') % (self.dest().source())
    
    def getTracker(self):
        '''
        return the linkTracker instance
        '''
        return self._tracker

    def record_packet_entry(self, packet, time):
        self._tracker.record_packet_entry(packet, time)
        
    def update_queueing_delay(self, packet, time):
        """
        Updates the queuing delay of the link.
        """

        self._tracker.update_queueing_delay(packet, time)
    
    def record_sent(self, time, size):
        """
        Records the time when a packet is sent.
        """
        self._tracker.record_sent(time, size)
        #print str(time) + " " + str(size)
        
    def record_packet_loss(self, time):
        """
        Records the time when a packet is lost.
        """

        self._tracker.record_packet_loss(time)
        
    def record_buffer_size(self, time, size):
        """
        Records the buffer size at a certain time.
        """

        self._tracker.record_buffer_size(time, size)

    def record_round_trip(self, time, rtt):
        """
        Records the round trip time at a certain time.
        """

        self._tracker.record_round_trip(time, rtt)

    def record_link_rate(self, time, rate):
        '''
        record the link rate at a certain time
        '''
        
        self._tracker.record_link_rate(time, rate)

    def throughput(self, since, until):
        """
        Returns the throughput of the link within the given time range.
        """

        occupancy = self._tracker.occupancy(since, until, self.delay())

        if (until - since) == 0:
            return 0
        else:
            return (float(occupancy) / float(until - since))

    def rtt(self, since=-1):
        """
        Returns the average round trip time of the link.
        """

        mean_rtt = self._tracker.mean_rtt(since)

        if mean_rtt == -1:
            return 3 * self.delay()

        return mean_rtt

    def timeout(self, since=-1):
        """
        Returns the timeout length of the link.
        """

        return (self.rtt(since) + 4 * sqrt(self._tracker.variance_rtt(since)))

    def delay(self, delay=None):
        """
        delay()      -> returns the delay

        delay(delay) -> sets the delay as the specified value and
                        returns this instance
        """

        if delay is None:
            return self._delay

        # Checks that delay is a float
        if not isinstance(delay, float):
            raise TypeError, 'delay must be a float'

        self._delay = delay
        self._tracker.set_delay(delay)
        return self

    def mean_queuing_delay(self, since):
        """
        Returns the average queuing delay since the specified time.
        """

        return self._tracker.get_average_queueing_delay(since)

    def cost(self, time):
        """
        Returns the static component of the cost.
        """

        static_cost = Link._STATIC * self.delay()

        since = time - Link._WINDOW
        dynamic_cost = Link._DYNAMIC * self.mean_queuing_delay(since)

        return (static_cost + dynamic_cost)

    def rate(self, rate=None):
        """
        rate()     -> returns the rate

        rate(rate) -> sets the rate as the specified value and returns
                      this instance
        """

        if rate is None:
            return self._rate

        # Checks that rate is an int
        if not isinstance(rate, int):
            raise TypeError, 'rate must be an int'

        self._rate = rate

    def dest(self, port=None):
        """
        dest()     -> returns the destination port

        dest(port) -> sets the destination port as the specified value
        """

        if port is None:
            return self._dest_port

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must be a Port instance'

        self._dest_port = port

class Port:
    """
    Builder for Port instances.
    """

    def __repr__(self):
        """
        Defines the string representation for a Port instance.
        """

        return ('Port['
                'source=%s, '
                'conn=%s'
                ']') % (self.source(), self.conn())

    def source(self, device=None):
        """
        source()       -> returns the source device

        source(device) -> sets the source device as the specified value
        """

        if device is None:
            return self._source_device

        # Checks that device is a Device instance
        if not isinstance(device, Device):
            raise TypeError, 'device must be a Device instance'

        self._source_device = device

    def conn(self, link=None):
        """
        conn()     -> returns the link connected to the destination

        conn(link) -> sets the link as the specified value
        """

        if link is None:
            return self._conn_link

        # Checks that link is a Link instance
        if not isinstance(link, Link):
            raise TypeError, 'link must be a Link instance'

        self._conn_link = link

    def incoming(self, queue=None):
        """
        incoming()      -> returns the queue for storing incoming packets

        incoming(queue) -> sets the queue as the specified value
        """

        if queue is None:
            return self._incoming_queue

        # Checks that queue is a Buffer instance
        if not isinstance(queue, Buffer):
            raise TypeError, 'queue must be a Buffer instance'

        self._incoming_queue = queue

    def outgoing(self, queue=None):
        """
        outgoing()      -> returns the queue for storing outgoing packets

        outgoing(queue) -> sets the queue as the specified value
        """

        if queue is None:
            return self._outgoing_queue

        # Checks that queue is a Buffer instance
        if not isinstance(queue, Buffer):
            raise TypeError, 'queue must be a Buffer instance'

        self._outgoing_queue = queue
