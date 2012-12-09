from math import sqrt

from device import Device
from event import Event
from packet import Packet
from trackers.flow import FlowTracker

class Flow:
    """
    Builder for Flow instances.
    """

    _NUM_DUPLICATES = 3

    _MARGIN = 5000

    def __init__(self, algorithm, window_size=1):
        """
        Creates a Flow instance with the specified congestion control
        algorithm.
        """

        # TODO: check that algorithm is a CongestionAlgorithm instance
        # if not isinstance(algorithm, CongestionAlgorithm):
        #     raise TypeError, 'algorithm must be a CongestionAlgorithm instance'

        self._algorithm = algorithm
        self.window(window_size)
        self.unack(0)

        self._num_bits = None
        self._start_time = None
        self._dest_device = None

        self._curr_seq_num = 0
        self._unack_packets = []

        self._ack_counts = {}

        self._last_timeout = -Flow._MARGIN
        self._last_duplicate = -Flow._MARGIN

        self._tracker = FlowTracker()

    def getTracker(self):
        '''
        return the flowTracker instance
        '''
        return self._tracker

    def record_packet_rtt(self, packet, time):
        self._tracker.record_packet_rtt(packet, time)

    def record_round_trip(self, time, rtt):
        """
        Records the round trip time at a certain time.
        """

        self._tracker.record_round_trip(time, rtt)

    def min_rtt(self, delay, since=-1):
        """
        Returns the minimum round trip time of the flow.
        """

        min_rtt = self._tracker.min_rtt(since)

        if min_rtt == -1:
            return 2 * delay

        return min_rtt

    def rtt(self, delay, since=-1):
        """
        Returns the average round trip time of the flow.
        """

        mean_rtt = self._tracker.mean_rtt(since)

        if mean_rtt == -1:
            return 3 * delay

        return mean_rtt
        
    def timeout(self, delay, since=-1):
        """
        Returns the timeout length of the flow.
        """

        return (self.rtt(delay, since) + 4 * sqrt(self._tracker.variance_rtt(since)))
        
    def is_able(self):
        """
        """

        return (self.window() > self.unack())

    def has_data(self):
        """
        """

        num_bits = self.bits()

        return (num_bits is None or num_bits > 0)

    def next_seq(self):
        """
        """

        self._curr_seq_num += 1

        return self._curr_seq_num

    def throughput(self, since, until, delay):
        """
        Returns the throughput of the link within the given time range.
        """

        occupancy = self.occupancy(since, until, delay)

        if (until - since) == 0:
            return 0
        else:
            return (float(occupancy) / float(until - since))
            
    def occupancy(self, since, until, delay):
        """
        Returns the number of packets in the link at the specified
        time.
        """

        total_size = 0

        for (time, size) in self._tracker.get_times_sent():
            if since < (time + delay) and until > time:
                initial = max(time, since)
                final = min(time + delay, until)

                part = float(final - initial) / float(delay)

                total_size += size * part

        return total_size
        
    def analyze(self, event, link):
        """
        Analyzes the specified event from the specified link.
        """

        action = event.action()
        time = event.scheduled()
        packet = event.packet()

        reset = False

        seq_num = packet.seq()

        #record starting window size
        windowsize = self.window()
        self._tracker.record_windowsize(time, windowsize)

        if action == Event._SEND and not packet.has_datum(Packet._ACK):
            self._tracker.record_sent(time, packet.size(), link.delay())

            self._unack_packets.append(packet.seq())

        elif action == Event._RECEIVE and packet.has_datum(Packet._ACK):
            seq_num = packet.seq()

            if seq_num in self._unack_packets:
                self._tracker.record_received(time)

                self._algorithm.handle_ack_received()

                self._unack_packets.remove(seq_num)
            else:
                num_acks = self._ack_counts.get(seq_num, 0) + 1
                self._ack_counts[seq_num] = num_acks

                if num_acks == Flow._NUM_DUPLICATES:
                    # Handles 3 duplicate acknowledgments received
                    if time > (self._last_duplicate + Flow._MARGIN):
                        print '[ATTN] [%.3f] 3 duplicate acks in %s' % (time, self._algorithm.state())

                        self._algorithm.handle_duplicate_acks(Flow._NUM_DUPLICATES)

                        self._last_duplicate = time

                    # self.bits(self.bits() + len(self._unack_packets) * Packet._DATA_SIZE)

                    self._unack_packets = []
                    self._curr_seq_num = seq_num - 1

                    reset = True

        elif action == Event._TIMEOUT:
            # Checks that packet was not already acknowledged
            if seq_num in self._unack_packets:
                # self.bits(self.bits() + len(self._unack_packets) * Packet._DATA_SIZE)

                self._unack_packets.remove(seq_num)

                if time > (self._last_timeout + Flow._MARGIN):
                    print '[ATTN] [%.3f] timeout in %s' % (time, self._algorithm.state())

                    self._algorithm.handle_timeout()

                    self._last_timeout = time

                self._unack_packets = []
                self._curr_seq_num = seq_num - 1

                self._ack_counts = {}

                reset = True

        num_unack = len(self._unack_packets)
        self.unack(num_unack)

        #record ending window size
        windowsize = self.window()
        self._tracker.record_windowsize(time, windowsize)

        return reset
        
    def prepare(self, packet):
        """
        Prepares the specified packet for sending.
        Attaches the sequence number.
        """

        # TODO: verify destination of packet

        packet.seq(self.next_seq())

        num_bits = self.bits()
        if num_bits is not None:
            self.bits(num_bits - packet.size())

    def window(self, size=None):
        """
        window()     -> returns the window size

        window(size) -> sets the window size as the specified value
        """

        if size is None:
            return self._window_size

        # Checks whether size is an int and converts to a float
        if isinstance(size, int):
            size = float(size)

        # Checks that size is a float
        if not isinstance(size, float):
            raise TypeError, 'window size must be a float'

        # Checks that size is positive
        elif size <= 0:
            raise ValueError, 'window size must be positive'

        self._window_size = size

    def unack(self, num=None):
        """
        unack()    -> returns the number of unacknowledged packets

        unack(num) -> sets the number of unacknowledged packets as the
                      specified value
        """

        if num is None:
            return self._num_unack

        # Checks that num is an int
        if not isinstance(num, int):
            raise TypeError, 'number of unacknowledged packets must be an int'

        # Checks that num is nonnegative
        elif num < 0:
            raise ValueError, 'number of unacknowledged packets must be nonnegative'

        self._num_unack = num
    
    def bits(self, num=None):
        """
        bits()    -> returns the number of bits

        bits(num) -> sets the number of bits
        """

        if num is None:
            return self._num_bits

        # Checks that num is an int
        if not isinstance(num, int):
            raise TypeError, 'number of bits must be an int'

        # Checks that num is nonnegative
        elif num < 0:
            raise ValueError, 'number of bits must be nonnegative'

        self._num_bits = num

    def start(self, time=None):
        """
        start()     -> returns the start time

        start(time) -> sets the start time as the specified value
        """

        if time is None:
            return self._start_time

        # Checks whether time is an int and converts to a float
        if isinstance(time, int):
            time = float(time)

        # Checks that time is a float
        if not isinstance(time, float):
            raise TypeError, 'scheduled time must be a float'

        self._start_time = time

    def dest(self, device=None):
        """
        dest()       -> returns the destination device

        dest(device) -> sets the destination device as the specified
                        value
        """

        if device is None:
            return self._dest_device

        # Checks that device is a Device instance
        if not isinstance(device, Device):
            raise TypeError, 'device must be a Device instance'

        self._dest_device = device
