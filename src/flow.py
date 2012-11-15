from device import Device
from flowTracker import FlowTracker

class Flow:
    """
    Builder for Flow instances.
    """

    def __init__(self, algorithm):
        """
        Creates a Flow instance with the specified congestion control
        algorithm.
        """

        # TODO: check that algorithm is a CongestionAlgorithm instance
        # if not isinstance(algorithm, CongestionAlgorithm):
        #     raise TypeError, 'algorithm must be a CongestionAlgorithm instance'

        self._algorithm = algorithm

        self._num_bits = None
        self._start_time = None
        self._dest_device = None

        self._curr_seq_num = 0

    def getTracker(self):
        '''
        return the flowTracker instance
        '''
        return self.tracker

    def is_able(self):
        """
        """

        return (self._algorithm.window() > self._algorithm.unack())

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
