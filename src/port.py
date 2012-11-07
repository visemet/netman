from collections import deque
from device import Device
from link import Link

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

        return 'Port[device=%s]' % (self.device())

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

    def device(self, device=None):
        """
        device()       -> returns the device

        device(device) -> sets the device as the specified value and
                          returns this instance
        """

        if device is None:
            return self._device

        # Checks that device is a Device instance
        if not isinstance(device, Device):
            raise TypeError, 'device must be a Device instance'

        self._device = device
        return self

    def in_queue(self, queue=None):
        """
        in_queue()      -> returns the queue for storing incoming
                           packets

        in_queue(queue) -> sets the queue as the specified value and
                           returns this instance
        """

        if queue is None:
            return self._in_queue

        # Checks that queue is a deque
        if not isinstance(queue, deque):
            raise TypeError, 'queue must be a deque'

        self._in_queue = queue
        return self

    def out_queue(self, queue=None):
        """
        out_queue()      -> returns the queue for storing outgoing
                            packets

        out_queue(queue) -> sets the queue as the specified value and
                            returns this instance
        """

        if queue is None:
            return self._out_queue

        # Checks that queue is a deque
        if not isinstance(queue, deque):
            raise TypeError, 'queue must be a deque'

        self._out_queue = queue
        return self

    def in_link(self, link=None):
        """
        in_link()     -> returns the link by which incoming packets are
                         received

        in_link(link) -> sets the link as the specified value and
                         returns this instance
        """

        if link is None:
            return self._in_link

        # Checks that link is a Link instance
        if not isinstance(link, Link):
            raise TypeError, 'link must be a Link instance'

        self._in_link = link
        return self

    def out_link(self, link=None):
        """
        out_link()     -> returns the link by which outgoing packets
                          are sent

        out_link(link) -> sets the link as the specified value and
                          returns this instance
        """

        if link is None:
            return self._out_link

        # Checks that link is a Link instance
        if not isinstance(link, Link):
            raise TypeError, 'link must be a Link instance'

        self._out_link = link
        return self
