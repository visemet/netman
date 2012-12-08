from algorithm import CongestionAlgorithm
from flow import Flow

class FAST(CongestionAlgorithm):
    """
    Logic for FAST TCP congestion algorithm.
    """

    _TYPE = 'fast'

    _SS = 'ss'
    _CA = 'ca'

    # Overrides CongestionAlgorithm.initialize(flow)
    def initialize(self, flow, ssthresh=1, gamma=0.1, alpha=50):
        """
        Initializes the congestion algorithm using the specified flow.
        """
        
        # Checks that flow is a Flow instance
        if not isinstance(flow, Flow):
            raise TypeError, 'flow must be a Flow instance'
            
        self._flow = flow

        self.state(FAST._SS)
        self.ssthresh(ssthresh)

        self._gamma = gamma
        self._alpha = alpha

    # Overrides CongestionAlgorithm.handle_ack_received()
    def handle_ack_received(self):
        """
        Handles a received acknowledgment.
        """

        cwnd = self._flow.window()
        state = self.state()

        ssthresh = self.ssthresh()

        # Currently in slow start
        if state == FAST._SS:
            cwnd += 1

            # Handle case where slow start threshold is exceeded
            if ssthresh != -1 and cwnd > ssthresh:
                # Go into congestion avoidance
                self.state(FAST._CA)

        # Currently in congestion avoidance
        elif state == FAST._CA:
            gamma = self._gamma
            alpha = self._alpha

            min_rtt = self._flow.min_rtt(10) # TODO: somehow get link delay
            rtt = self._flow.rtt(10) # TODO: somehow get link delay

            cwnd =  min(2 * cwnd, (1 - gamma) * cwnd + gamma * ((float(min_rtt) / float(rtt)) * cwnd + alpha))

        self._flow.window(cwnd)

    # Overrides CongestionAlgorithm.handle_timeout()
    def handle_timeout(self):
        """
        Handles a timeout.
        """

        cwnd = self._flow.window()

        # Sets the state to slow start
        self.state(FAST._SS)

        # Sets the slow start threshold as half the current window size
        ssthresh = max(float(cwnd) / 2.0, 1)
        self.ssthresh(ssthresh)

        # Sets the window size to one
        self._flow.window(1)

    def handle_duplicate_acks(self, num=3):
        """
        Handles n-duplicate acknowledgments.
        """

        # Checks that num is an int
        if not isinstance(num, int):
            raise TypeError, 'num must be an int'

        # Checks that num is nonnegative
        elif num < 0:
            raise ValueError, 'num must be nonnegative'

        if self.state() == FAST._CA:
            cwnd = self._flow.window()

            # Sets the window size as half the current window size 
            cwnd = max(float(cwnd) / 2.0, 1)

            # Sets the slow start threshold as half the current window size
            self.ssthresh(cwnd)

            self._flow.window(cwnd + num)

    def ssthresh(self, ssthresh=None):
        """
        ssthresh()         -> returns the slow start threshold

        ssthresh(ssthresh) ->  sets the slow start threshold as the
                               specified value
        """

        if ssthresh is None:
            return self._ssthresh

        # Converts ssthresh from an int to float
        if isinstance(ssthresh, int):
            ssthresh = float(ssthresh)

        # Checks that ssthresh is a float
        elif not isinstance(ssthresh, float):
            raise TypeError, 'ssthresh must be a float'

        # Checks that ssthresh is nonnegative
        elif ssthresh < 0:
            raise ValueError, 'ssthresh must be nonnegative'

        self._ssthresh = ssthresh 

    def state(self, state=None):
        """
        state()      ->  returns the state

        state(state) ->  sets the state as the specified value
        """
    
        if state is None:
            return self._state

        self._state = state
