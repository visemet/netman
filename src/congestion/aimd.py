from algorithm import CongestionAlgorithm
from flow import Flow

class AIMD(CongestionAlgorithm):
    """
    Logic for Additive Increase, Multiplicative Decrease algorithm.
    """

    # Overrides CongestionAlgorithm.initialize(flow)
    def initialize(self, flow):
        """
        Initializes the congestion algorithm using the specified flow.
        """

        # Checks that flow is a Flow instance
        if not isinstance(flow, Flow):
            raise TypeError, 'flow must be a Flow instance'

        self._flow = flow

    # Overrides CongestionAlgorithm.handle_ack_received()
    def handle_ack_received(self):
        """
        Handles a received acknowledgment.
        """

        self._flow.window(self._flow.window() + 1.0 / self._flow.window())

    # Overrides CongestionAlgorithm.handle_dropped_packet()
    def handle_packet_dropped(self):
        """
        Handles a dropped packet.
        """

        self._flow.window(self._flow.window() / 2.0)
