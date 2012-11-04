from packet import Packet

class Event:
    """
    """

    def __init__(self, time, packet):
        """
        Creates an Event instance with the specified time and packet.
        """

        self.schedule(time)
        self.packet(packet)

    def schedule(self, time=None):
        """
        schedule()     -> returns the time

        schedule(time) -> sets the time as the specified value
        """

        if time is None:
            return self._time

        # Checks that time is a float
        if not isinstance(time, float):
            raise TypeError, 'time must be a float'

        self._time = time

    def packet(self, packet=None):
        """
        packet()       -> returns the packet

        packet(packet) -> sets the packet as the specified value
        """

        if packet is None:
            return self._packet

        # Checks that packet is a Packet instance
        if not isinstance(packet, Packet):
            raise TypeError, 'packet must a Packet instance'

        self._packet = packet
