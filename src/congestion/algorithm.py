class CongestionAlgorithm:
    """
    Base class for congestion algorithms.
    """

    def initialize(self, flow):
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
