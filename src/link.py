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
        return self

    def source(self, port=None):
        """
        source()     -> returns the source port

        source(port) -> sets the source port as the specified value
                        and returns this instance
        """

        if port is None:
            return self._source

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must be a Port instance'

        self._source = port
        return self

    def destination(self, port=None):
        """
        destination()     -> returns the destination port

        destination(port) -> sets the destination port as the specified
                             value and returns this instance
        """

        if port is None:
            return self._destination

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must be a Port instance'

        self._destination = port
        return self
