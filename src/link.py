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

    def source(self, source=None):
        """
        source()       -> returns the source

        source(source) -> sets the source as the specified value and
                          returns this instance
        """

        if source is None:
            return self._source

        # Checks that source is a Device instance
        if not isinstance(source, Device):
            raise TypeError, 'source must be a Device instance'

        self._source = source
        return self

    def destination(self, destination=None):
        """
        destination()            -> returns the destination

        destination(destination) -> sets the destination as the
                                    specified value and returns this
                                    instance
        """

        if destination is None:
            return self._destination

        # Checks that destination is a Device instance
        if not isinstance(destination, Device):
            raise TypeError, 'destination must be a Device instance'

        self._destination = destination
        return self
