from device import Device
from flowTracker import FlowTracker

class Flow:
    """
    """

    def __init__(self, num_bits, start_time, destination, algorithm):
        """
        Creates a Flow instance with the specified number of bits,
        start time, destination, and algorithm.
        """

        self.bits(num_bits)
        self.schedule(start_time)
        self.destination(destination)
        # self.algorithm(algorithm)
        # self.tracker(FlowTracker())

    def getTracker(self):
        '''
        return the flowTracker instance
        '''
        return self.tracker
    
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
        # elif num <= 0:
        #     raise ValueError, 'number of bits must be positive'

        self._num_bits = num

    def schedule(self, time=None):
        """
        schedule()     -> returns the start time

        schedule(time) -> sets the start time
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

    def destination(self, destination=None):
        """
        destination()            -> returns the destination

        destination(destination) -> sets the destination
        """

        if destination is None:
            return self._destination

        # Checks that destination is a Device instance
        if not isinstance(destination, Device):
            raise TypeError, 'destination must be a Device instance'

        self._destination = destination
