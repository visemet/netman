from port import Port

class Event:
    """
    Builder for Event instances.
    """

    _SEND = 'send'
    _RECEIVE = 'receive'

    def __init__(self, time, port, action):
        """
        Creates an Event instance with the specified time and the
        specified port.
        """

        self.schedule(time)
        self.port(port)
        self.action(action)

    def __lt__(self, other):
        """
        """

        return self.schedule() < other.schedule()

    def __le__(self, other):
        """
        """

        return self.schedule() <= other.schedule()

    def __eq__(self, other):
        """
        """

        return self.schedule() == other.schedule()

    def __ne__(self, other):
        """
        """

        return self.schedule() != other.schedule()

    def __gt__(self, other):
        """
        """

        return self.schedule() > other.schedule()

    def __ge__(self, other):
        """
        """

        return self.schedule() >= other.schedule()

    def __str__(self):
        """
        """

        return 'Event[time=%s, port=%s]' % (self.schedule(), self.port())

    def schedule(self, time=None):
        """
        schedule()     -> returns the time

        schedule(time) -> sets the time as the specified value
        """

        if time is None:
            return self._time

        # Checks whether time is an int and converts to float
        if isinstance(time, int):
            time = float(time)

        # Checks that time is a float
        if not isinstance(time, float):
            raise TypeError, 'time must be a float'

        self._time = time

    def port(self, port=None):
        """
        port()     -> returns the port

        port(port) -> sets the port as the specified value
        """

        if port is None:
            return self._port

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must a Port instance'

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
            raise TypeError, 'action must a string'

        self._action = action
