class Port:
    """
    """

    def __init__(self, in_queue, out_queue, in_link, out_link):
        """
        Creates a Port instance with the specified queues and links.
        """

        # TODO: Check in_queue isinstance(collections.deque)
        self._in_queue = in_queue

        # TODO: Check out_queue isinstance(collections.deque)
        self._out_queue = out_queue

        # TODO: Check in_link isinstance(link.Link)
        self._in_link = in_link

        # TODO: Check out_link isinstance(link.Link)
        self._out_link = out_link

    def in_queue(self):
        """
        Returns the queue storing incoming packets.
        """

        return self._in_queue

    def out_queue(self):
        """
        Returns the queue storing outgoing packets.
        """

        return self._out_queue

    def in_link(self):
        """
        Returns the link by which incoming packets are received.
        """

        return self._in_link

    def out_link(self):
        """
        Returns the link by which outgoing packets are sent.
        """

        return self._out_link
