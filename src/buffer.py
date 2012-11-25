from collections import deque

from packet import Packet

class Buffer:
    """
    """

    def __init__(self, max_size):
        """
        """

        self._max_size = max_size

        self._curr_size = 0
        self._deque = deque()

    def __len__(self):
        """
        """

        return len(self._deque)

    def has_space(self, packet):
        """
        """

        # Checks that packet is a Packet instance
        if not isinstance(packet, Packet):
            raise TypeError, 'packet must be a Packet instance'

        return (self._curr_size + packet.size() <= self._max_size)

    def append(self, packet):
        """
        """

        # Checks that packet is a Packet instance
        if not isinstance(packet, Packet):
            raise TypeError, 'packet must be a Packet instance'

        if self.has_space(packet):
            self._deque.append(packet)
            self._curr_size += packet.size()

    def popleft(self):
        """
        """

        packet = self._deque.popleft()
        self._curr_size -= packet.size()

        return packet
