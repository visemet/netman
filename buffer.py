from collections import deque

from packet import Packet

class Buffer:
    """
    Builder for Buffer instances.
    """

    def __init__(self, max_size):
        """
        Creates a Buffer instance with the specified maximum size.
        """

        self._max_size = max_size

        self._curr_size = 0
        self._deque = deque()

    def __len__(self):
        """
        Returns the length of the buffer.
        """

        return len(self._deque)

    def size(self):
        """
        Returns the size of the buffer.
        """

        return self._curr_size

    def has_space(self, packet):
        """
        Returns True if the buffer has space for the specified packet,
        and False otherwise.
        """

        # Checks that packet is a Packet instance
        if not isinstance(packet, Packet):
            raise TypeError, 'packet must be a Packet instance'

        return (self.size() + packet.size() <= self._max_size)

    def append(self, packet):
        """
        Adds the specified packet to the tail of the buffer.
        """

        # Checks that packet is a Packet instance
        if not isinstance(packet, Packet):
            raise TypeError, 'packet must be a Packet instance'

        if self.has_space(packet):
            self._deque.append(packet)
            self._curr_size += packet.size()

    def peekleft(self):
        """
        Returns the packet at the head of the buffer.
        """

        packet = None
        if self._deque:
            packet = self._deque[0]

        return packet

    def popleft(self):
        """
        Removes and returns the packet at the head of the buffer.
        """

        packet = self._deque.popleft()
        self._curr_size -= packet.size()

        return packet
