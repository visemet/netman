from conn import Port
from packet import Packet

class Event:
    """
    Builder for Event instances.
    """

    _CREATE = 'create'
    _RECEIVE = 'receive'
    _SEND = 'send'
    _TIMEOUT = 'timeout'

    def __init__(self):
        """
        Creates an Event instance with the specified time and the
        specified port.
        """

        self._scheduled_time = None
        self._port = None
        self._action = None
        self._packet = None

    def __lt__(self, other):
        """
        Defines the condition for when an Event instance is less than
        another.
        """

        return (self.scheduled() < other.scheduled())

    def __le__(self, other):
        """
        Defines the condition for when an Event instance is less than
        or equal to another.
        """

        return (self < other or self == other)

    def __eq__(self, other):
        """
        Defines the condition for when an Event instance is equal to
        another.
        """

        return (self.scheduled() == other.scheduled()
                and self.port() == other.port()
                and self.action() == other.action()
                and self.packet() == other.packet())

    def __ne__(self, other):
        """
        Defines the condition for when an Event instance is not equal
        to another.
        """

        return (not self == other)

    def __gt__(self, other):
        """
        Defines the condition for when an Event instance is greater
        than another.
        """

        return (self.scheduled() > other.scheduled())

    def __ge__(self, other):
        """
        Defines the condition for when an Event instance is greater
        than or equal to another.
        """

        return (self > other or self == other)

    def __repr__(self):
        """
        Defines the string representation for an Event instance.
        """

        return ('Event['
                'schedule=%s, '
                'port=%s, '
                'action=%s'
                ']') % (self.scheduled(), self.port(), self.action())

    def scheduled(self, time=None):
        """
        scheduled()     -> returns the scheduled time

        scheduled(time) -> sets the scheduled time as the specified
                           value
        """

        if time is None:
            return self._scheduled_time

        # Checks whether time is an int and converts to float
        if isinstance(time, int):
            time = float(time)

        # Checks that time is a float
        if not isinstance(time, float):
            raise TypeError, 'time must be a float'

        self._scheduled_time = time

    def port(self, port=None):
        """
        port()     -> returns the port

        port(port) -> sets the port as the specified value
        """

        if port is None:
            return self._port

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must be a Port instance'

        self._port = port

    def action(self, action=None):
        """
        action()       -> returns the action

        action(action) -> sets the action as the specified value
        """

        if action is None:
            return self._action

        # Checks that action is a string
        if not isinstance(action, str):
            raise TypeError, 'action must be a string'

        self._action = action

    def packet(self, packet=None):
        """
        packet()       -> returns the packet

        packet(packet) -> sets the packet as the specified value
        """

        if packet is None:
            return self._packet

        # Checks that packet is a Packet instance
        if not isinstance(packet, Packet):
            raise TypeError, 'packet must be a Packet instance'

        self._packet = packet
