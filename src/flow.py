from device import Device
from event import Event
from packet import Packet
from trackers.flow import FlowTracker

class Flow:
    """
    Builder for Flow instances.
    """

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

        self._tracker = FlowTracker()

    def getTracker(self):
        '''
        return the flowTracker instance
        '''
        return self.tracker

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

    def analyze(self, event):
        """
        """

        action = event.action()
        time = event.scheduled()
        packet = event.packet()

        if action == Event._SEND and not packet.has_datum(Packet._ACK):
            self._tracker.record_sent(time)
        elif action == Event._RECEIVE and packet.has_datum(Packet._ACK):
            self._tracker.record_received(time)

    def prepare(self, packet):
        """
        Prepares the specified packet for sending.
        Attaches the sequence number.
        """

        # TODO: verify destination of packet

        packet.seq(self.next_seq())

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

        # Checks that num is positive
        elif num <= 0:
            raise ValueError, 'number of bits must be positive'

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
