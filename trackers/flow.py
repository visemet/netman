from device import Device

class FlowTracker:
    """
    Builder for FlowTracker instances.
    """

    def __init__(self):
        """
        Creates a new FlowTracker instance with 
            _times_sent = []
            _times_received = []
            _flowrates = []
            _window_sizes = []
            lists are lists of times at which the packet was sent or received
            
        """

        self._times_sent = []       # list of (time, size)
        self._times_received = []   # list of time
        self._flowrates = []        # list of (time, rate)
        self._window_sizes = []     # list of (time, size)

        self._packetsSent = 0
        self._packetsReceived = 0

    def get_times_sent(self):
        return self._times_sent

    def record_sent(self, time, size):
        """
        Adds an entry in the history to indicate a packet was sent at
        the specified time.
        """

        self._times_sent.append((time, size))

    def record_received(self, time):
        """
        Adds an entry in the history to indicate a packet was received
        at the specified time.
        """

        self._times_received.append(time)

    def packetSent(self, time):
        """
        adds a time log of when a packet was sent
        """
        self._packetsSent.append(time)

    def numPacketsSent(self):
        '''
            return the total number of packets sent
        '''
        return len(self._times_sent)
   
    def packetReceived(self, time):
        '''
        adds a time log of when a packet was received
        '''
        self._packetsReceived.add(time)
        
    def numPacketsReceived(self):
        '''
        return the total number of packets received
        '''
        return len(self._times_received)
    
    
    '''
    def sendRate(self):
        
        
        if (self._times_sent[len(self._times_sent)-1] - self._times_sent[0]) == 0:
            return 0
        else:
            return self.numPacketsSent()/  \
            (self._times_sent[len(self._times_sent)-1] - self._times_sent[0]) #TODO should start time be 0?
                
    def receiveRate(self):
        
        
        if (self.packetsReceived[len(self._times_received)-1] - self.packetsReceived[0]) == 0:
            return 0
        else:
            return self.numPacketsReceived()/  \
            (self.packetsReceived[len(self._times_received)-1] - self.packetsReceived[0]) # TODO should start time be 0?
    
    '''
    
    '''
    return second to last flow rate data point.
    if this is being called for the first time, then return 0,0
    '''
    def get_previous_flowrate_point(self):
        if len(self._flowrates) < 2:
            return 0
        else:
            return self._flowrates[len(self._flowrates) -2][0]
        
    def occupancy(self, since, until):
        """
        Returns the number of packets in the link at the specified
        time.
        """

        total_size = 0

        for (time, size) in self._times_sent:
            if since < time and until > time:
                initial = max(time, since)
                final = min(time, until)

                part = float(final - initial) / float(delay)

                total_size += size * part

        return total_size
    
    def throughput(self, since, until):
        """
        Returns the throughput of the link within the given time range.
        """

        occupancy = self.occupancy(since, until, self._delay)

        if (until - since) == 0:
            return 0
        else:
            return (float(occupancy) / float(until - since))

    def packetDelay(self):
        '''
        return the average packet delay
        '''
        #TODO is this the average of the distance between corresponding send and receive times?
        packetDelay = 0
        return packetDelay
        
    def record_flowrate(self, time, rate):
        '''
            record (time, flowrate)
        '''
        self._flowrates.append((time, rate))
        
    def get_flow_rate_data(self):
        returnValue = self._flowrates
        returnValue.sort()
        return returnValue
        
    def record_windowsize(self, time, size):
        '''
            record (time, size)
        '''
        self._window_sizes.append((time, size))
        
    def get_window_size_data(self):
        self._window_sizes.sort()
        return self._window_sizes

