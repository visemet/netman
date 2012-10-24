class Device:
    """
    Base class for routers and hosts.
    """

    def initialize(self):
        """
        Initializes the device. Implemented in each subclass.
        """

        raise NotImplementedError('Device.initialize()')

    def send(self, packet):
        """
        Sends the specified packet. Implemented in each subclass.
        """

        raise NotImplementedError('Device.send(packet)');

    def process(self, event):
        """
        Processes the specified event. Implemented in each subclass.
        """
        
        raise NotImplementedError('Device.process(event)')
