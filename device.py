class Device:
    """
    Base class for routers and hosts.
    """

    def __init__(self, name):
        """
        Creates a device instance with the specified name.
        """

        # Checks that name is a string
        if not isinstance(name, str):
            raise TypeError, 'name must be a string'

        self._id = name

    def __str__(self):
        """
        Defines the pretty print representation for a Device instance.
        """

        return self._id

    def __repr__(self):
        """
        Defines the string representation for a Device instance.
        """

        return ('Device['
                'id=%s'
                ']') % (self._id)

    def enable(self, port):
        """
        Enables the device to use the specified port. Implemented in
        each subclass.
        """

        raise NotImplementedError, 'Device.enable(port)'

    def initialize(self):
        """
        Initializes the device. Implemented in each subclass.
        """

        raise NotImplementedError, 'Device.initialize()'

    def process(self, event):
        """
        Processes the specified event. Implemented in each subclass.
        """
        
        raise NotImplementedError, 'Device.process(event)'
