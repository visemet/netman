from device import Device
from flow import Flow
from port import Port
from router import Router

class Host(Device):
    """
    Builder for Host instances.
    """

    def __init__(self, identifier):
        """
        Creates a Host instance with the specified port and the
        specified identifier.
        """

        Device.__init__(self, identifier)

        self._flows = set()

    def port(self, port):
        """
        Replaces the port with the specified value.
        """

        # Checks that port is a Port instance
        if not isinstance(port, Port):
            raise TypeError, 'port must be a Port instance'

        self._port = port
    
    def connect(self, flow):
        """
        Adds the specified flow to the set of flows.
        """

        # Checks that flow is a Flow instance
        if not isinstance(flow, Flow):
            raise TypeError, 'flow must be a Flow instance'

        self._flows.add(flow)

    # Overrides Device.initialize()
    def initialize(self):
        """
        Initializes the host.
        """

        raise NotImplementedError, 'Host.initialize()'

    # Overrides Device.send(packet)
    def send(self, packet):
        """
        Sends the specified packet.
        """

        raise NotImplementedError, 'Host.send(packet)'

    # Overrides Device.process(event)
    def process(self, event):
        """
        Processes the specified event.
        """
        
        raise NotImplementedError, 'Host.process(event)'
