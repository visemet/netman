class Event:
    """
    """

    def __init__(self, schedule, packet):
        """
        Creates an Event instance with the specified schedule and packet.
        """

        # TODO: Check schedule isinstance(float)
        self._schedule = schedule

        # TODO: Check packet isinstance(packet.Packet)
        self._packet = packet

    def schedule(self):
        """
        Returns the scheduled time.
        """

        return self._schedule

    def packet(self):
        """
        Returns the packet.
        """

        return self._packet
