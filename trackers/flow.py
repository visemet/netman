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
        
        #RTT
        self._avg_rtt = 0
        self._rtts = []             # list of (time, rtt)
        self._current_rtt = 0
    
    #get the rtt for a packet
    def record_packet_rtt(self, packet, time):
        val = time - packet.get_create_time()
        self._rtts.append((time, val))
        return val

    def mean_rtt(self, since):
        """
        Returns the average round trip time since the specified time.
        """

        sum_rtt = 0
        count_rtt = 0

        for (time, rtt) in reversed(self._rtts):
            if time < since:
                break

            sum_rtt += rtt
            count_rtt += 1

        if count_rtt == 0:
            return -1

        return (float(sum_rtt) / float(count_rtt))
    
    # return the average rtt
    def get_average_rtt(self):
        count = 0
        sum = 0
        for time, i in self._rtts:
            sum += i
            count += 1
        return (sum*1.0) / count
        
    def variance_rtt(self, since):
        """
        Returns the variance in the round trip time since the specified
        time.
        """

        sum_square_deviations = 0
        count_square_deviations = 0

        mean_rtt = self.mean_rtt(since)

        for (time, rtt) in reversed(self._rtts):
            if time < since:
                break

            sum_square_deviations += (rtt - mean_rtt) ** 2
            count_square_deviations += 1

        if count_square_deviations == 0:
            return 0

        return (float(sum_square_deviations) / float(count_square_deviations))   

    def get_times_sent(self):
        return self._times_sent

    def record_sent(self, time, size, delay):
        """
        Adds an entry in the history to indicate a packet was sent at
        the specified time.
        """

        self._times_sent.append((time, size, delay))

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

        for time, size, delay in self._times_sent:
            if since < (time+delay) and until > time:
                initial = max(time, since)
                final = min(time+delay, until)

                part = float(final - initial) / float(delay)

                total_size += size * part

        return total_size

    def occupancy(self, since, until, by):
        """
        Returns the number of packets in the link at the specified
        time.
        """

        total_size = 0

        index = 0
        length = len(self._times_sent)

        go_back = -1

        while index < length:
            (time, size, delay) = self._times_sent[index]

            if until < time:
                break
            elif since > (time + delay):
                index += 1
            elif go_back == -1 and (since + by) < (time + delay):
                go_back = index

            if since < (time + delay) and (since + by) > time:
                initial = max(time, since)
                final = min(time + delay, since + by)
        
                part = float(final - initial) / float(delay)
        
                total_size += size * part

                index += 1
            else:
                yield total_size

                index = go_back
                go_back = -1
                
                total_size = 0
                since += by

        yield total_size
    
    def throughput(self, since, until, by):
        """
        Returns the throughput of the link within the given time range.
        """

        if (until - since) == 0:
            yield 0
        else:
            for occupancy in self.occupancy(since, until, by):
                yield (float(occupancy) / float(by))

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
        """
        Returns the flow rate data.
        """

        since = 0
        until = self._times_sent[-1][0] # (time, size, delay)
        by = 1

        result = []

        for throughput in self.throughput(since, until, by):
            result.append((since, throughput))
            since += by

        return result
        
    def record_windowsize(self, time, size):
        '''
            record (time, size)
        '''
        self._window_sizes.append((time, size))
        
    def get_window_size_data(self):
        return self._window_sizes
        
    def get_rtt_data(self):
        return self._rtts

