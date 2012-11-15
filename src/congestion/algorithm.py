class CongestionAlgorithm:
    """
    Base class for congestion algorithms.
    """

    def initialize(self, flow, cwnd, awnd, ssthresh, gamma=None, alpha=None):
        """
        Initializes the congestion algorithm using the specified flow.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'CongestionAlgorithm.initialize(flow)'

    def handle_ack_received(self):
        """
        Handles a received acknowledgment.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'CongestionAlgorithm.handle_ack_received()'

    def handle_packet_dropped(self):
        """
        Handles a dropped packet.
        Implemented in each subclass.
        """

        raise NotImplementedError, 'CongestionAlgorithm.handle_dropped_packet()'
    
    def Handle3DupAck(self, ndup):
        pass

    def WindowDeflate(self, ssthresh):
        pass
    
    def ssthresh(self, ssthresh=None):
        pass
    
    def Initssthresh(self, Initssthresh=None):
        pass
        
    def awnd(self, awnd=None):
        pass
    
    def cwnd(self, cwnd=None): 
        pass
    
    def state(self, state=None):
        pass
