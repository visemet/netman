from algorithm import CongestionAlgorithm
# from flow import Flow

class AIMD(CongestionAlgorithm):
    """
    Logic for Additive Increase, Multiplicative Decrease algorithm.
    """

    # Overrides CongestionAlgorithm.initialize(flow)
    def initialize(self, flow, cwnd, awnd, ssthresh, gamma=None, alpha=None):
        """
        Initializes the congestion algorithm using the specified flow.
        """

        # Checks that flow is a Flow instance
        if not isinstance(flow, Flow):
            raise TypeError, 'flow must be a Flow instance'

        self._flow = flow
        
        if (gamma is None) & (alpha is None) :
            # set value of cwnd, awnd and ssthresh
            self._flow.window(cwnd)
            self.awnd(awnd)
            self.ssthresh(ssthresh)
            self.Initssthresh(ssthresh)
            self.state('SS')
        else :
            raise ValueError, 'not a valid argument'

    # Overrides CongestionAlgorithm.handle_ack_received()
    def handle_ack_received(self):
        """
        Handles a received acknowledgment.
        """
            # Get current cwnd and check if the state is 
            # SS or CA
        cwnd = self._flow.window()
        prev_state = self.state()
            
        if (prev_state is 'SS') & (cwnd > self.ssthresh()):
            self.state('CA')    
            self._flow.window(1)
        elif (cwnd > self.ssthresh()):
            self.state('SS')
            self._flow.window(1)
        elif self.state() is 'SS':
            self._flow.window(cwnd + 1)
        elif self.state() is 'CA':
            self._flow.window(cwnd + float(1)/float(cwnd))
                
    # Overrides CongestionAlgorithm.handle_dropped_packet()
    def handle_packet_dropped(self):
        """
        Handles a dropped packet.
        """

        cwnd = self.cwnd()      

        if self.state() is 'CA':                       
            self._flow.window(float(cwnd)/float(2))  

    def Handle3DupAck(self, ndup):
        """
        reset slow start threshold and inflate window
        """

        # check if ndup is positive and integer
        if not isinstance(ndup, int):
            raise TypeError, 'ndup must be integer'
        if ndup < 0:
            raise ValueError, 'ndup must be positivesemidefinite'

        newssthresh = float(self._flow.window())/float(2)
        self.ssthresh(max(newssthresh, 2))
        self._flow.window(self.ssthresh() + ndup)
    
    def WindowDeflate(self, ssthresh):
        """
        Reset window size to threshold after Handle3DupAck.
        This function is called 1RTT after new packet is transmit
        """
        self._flow.window(self.ssthresh())

        # Reset slow start threshold to the beginning
        self.ssthresh(self.Initssthresh())

    def ssthresh(self, ssthresh=None):
        """
    ssthresh()                 -> returns the ssthresh

        ssthresh(ssthresh)          ->  sets the ssthresh as the specified
                                     value and returns this instance
        """

        if ssthresh is None:
            return self._ssthresh

        # Checks that ssthresh is positive
        elif ssthresh<= 0:
            raise ValueError, 'ssthresh must be positive'

        self._ssthresh = ssthresh

    def Initssthresh(self, Initssthresh=None):
        """
        Initssthresh()                 -> returns the ssthresh

        Initssthresh(Initssthresh)          ->  sets the ssthresh as the specified
                                     value and returns this instance
        """

        if Initssthresh is None:
            return self._Initssthresh

        # Checks that ssthresh is positive
        elif Initssthresh<= 0:
            raise ValueError, 'ssthresh must be positive'

        self._Initssthresh = Initssthresh
            
    def awnd(self, awnd=None): 
        """
        awnd()                     ->  returns awnd

        awnd(awnd)                   ->  sets the awnd as the specified
                                    value and returns this instance
        """

        if awnd is None:
            return self._awnd

        # Checks that awnd is positivesemidefinite
        if awnd< 0:
            raise ValueError, 'awnd must be positivesemidefinite'
            
        self._awnd = awnd
        
    def cwnd(self, cwnd=None): 
        """
        cwnd()                     ->  returns cwnd

        cwnd(cwnd)                   ->  sets the cwnd as the specified
                                    value and returns this instance
        """

        if cwnd is None:
            return self._cwnd

        # Checks that cwnd is positivesemidefinite
        if cwnd<  0:
            raise ValueError, 'cwnd must be positivesemidefinite'

        self._cwnd = cwnd    

    def state(self, state=None):
        """
        state()                     ->  returns state

        state(state)                   ->  sets the state as the specified
                                    value and returns this instance
        """
    
        if state is None:
            return self._state

        self._state = state
