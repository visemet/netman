from collections import deque
from link import Link

class Port:
    """
    Builder for Port instances.
    """

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
