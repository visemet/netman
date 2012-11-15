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

    def WindowDeflate(self, ssthresh):
    
    def ssthresh(self, ssthresh=None):
    
    def Initssthresh(self, Initssthresh=None):
        
    def awnd(self, awnd=None):
    
    def cwnd(self, cwnd=None): 
    
    def state(self, state=None):
    
