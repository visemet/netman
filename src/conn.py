from collections import deque
from device import Device
from linkTracker import LinkTracker

class Link:
    """
    Builder for Link instances.
    """

    def initTracker(self):
        '''
        initialize the linkTracker
        '''
        self._tracker = LinkTracker()
        return self
    
    def getTracker(self):
        '''
        return the linkTracker instance
        '''
        return self._tracker
    
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
        return self

    def cost(self):
        """
        Returns the static component of the cost.
        """

        return self.delay() # TODO: + average queuing delay

    def rate(self, rate=None):
        """
        rate()     -> returns the rate

        rate(rate) -> sets the rate as the specified value and returns
                      this instance
        """

        if rate is None:
            return self._rate

        # Checks that rate is a float
        if not isinstance(rate, float):
            raise TypeError, 'rate must be a float'

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

    def __init__(self, window_size=1):
        """
        Creates a Port instance with the specified window size.
        """

        self.window(window_size)

    def __str__(self):
        """
        """

        return 'Port[device=%s->%s]' % (self.device(), self.out_link().destination().device())

    def __repr__(self):
        """
        """

        return self.__str__()

    def window(self, size=None):
        """
        window()     -> returns the window size

        window(size) -> sets the window size as the specified value
        """

        if size is None:
            return self._window_size

        # Checks that size is an int
        if not isinstance(size, int):
            raise TypeError, 'window size must be an int'

        # Checks that size is positive
        elif size <= 0:
            raise ValueError, 'window size must be positive'

        self._window_size = size

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

        # Checks that queue is a deque
        if not isinstance(queue, deque):
            raise TypeError, 'queue must be a deque'

        self._incoming_queue = queue

    def outgoing(self, queue=None):
        """
        outgoing()      -> returns the queue for storing outgoing packets

        outgoing(queue) -> sets the queue as the specified value
        """

        if queue is None:
            return self._outgoing_queue

        # Checks that queue is a deque
        if not isinstance(queue, deque):
            raise TypeError, 'queue must be a deque'

        self._outgoing_queue = queue

    def algorithm(self, algorithm=None):
        """
        algorithm()          -> returns the algorithm

        algorithm(algorithm) -> sets the algorithm
        """

        if algorithm is None:
            return self._algorithm

        # TODO: check that algorithm isinstance(congestion.algorithm)
        self._algorithm = algorithm
