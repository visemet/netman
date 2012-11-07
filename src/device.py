class Device:
    """
    Base class for routers and hosts.
    """

    def __init__(self, identifier):
        """
        Creates a device instance with the specified identifier.
        """

        # Checks that identifier is a string
        if not isinstance(identifier, str):
            raise TypeError, 'identifier must be a string'

        self._id = identifier

    def __str__(self):
        """
        """

        return self._id

    def initialize(self):
        """
        Initializes the device. Implemented in each subclass.
        """

        raise NotImplementedError, 'Device.initialize()'

    def send(self, packet):
        """
        Sends the specified packet. Implemented in each subclass.
        """

        raise NotImplementedError, 'Device.send(packet)'

    def process(self, event):
        """
        Processes the specified event. Implemented in each subclass.
        """
        
        raise NotImplementedError, 'Device.process(event)'
