from port import Port

class Event:
    """
    Builder for Event instances.
    """

    def __init__(self, time, port):
        """
        Creates an Event instance with the specified time and the
        specified port.
        """

        self.schedule(time)
        self.port(port)

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
