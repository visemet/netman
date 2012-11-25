from buffer import Buffer
from device import Device
from trackers.link import LinkTracker

class Link:
    """
    Builder for Link instances.
    """

    def __repr__(self):
        """
        Defines the string representation for a Link instance.
        """

        return ('Link['
                'dest=%s'
                ']') % (self.dest().source())

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
