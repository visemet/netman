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

    def min_rtt(self, since):
        """
        Returns the minimum round trip time since the specified time.
        """

        min_rtt = -1

        for (time, rtt) in reversed(self._rtts):
            if time < since:
                break

            if min_rtt == -1 or rtt < min_rtt:
                min_rtt = rtt

        return min_rtt

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

        if count_square_deviations <= 1:
            return 10

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
            result.append((since + by, throughput))
            since += by
        '''
        everySecond = []
        currVal = 0
        currTime = 0
        for time, size in result:
            if (time / 250) == currTime:
                currVal = max(currVal, size)
            else:
                everySecond.append((currTime*250, currVal))
                currTime = (time / 250)   
                currVal = size
        return everySecond
        
        everySecond = []
        currVal = 0
        currTime = 0
        currSum = 0
        currCount = 0
        for time, size in result:
            if (time / 500) == currTime:
                currSum += size
                currCount += 1
            else:
                currVal = (currSum * 1.0) / currCount
                everySecond.append((currTime, currVal))
                currTime = (time / 500)   
                currSum = size
        return everySecond
        
        everySecond = []
        currCount = 0
        for time, size in result:
            if (currCount % 100)==0:
                everySecond.append((time, size))
            currCount += 1
        return everySecond
        '''
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

    def get_avg_throughput(self):
        result = self.get_flow_rate_data()
        sum = 0
        count = 0
        for time, throughput in result:
            sum += throughput
            count += 1
        print "avg throughput ", (sum*1.0)/count
        return (sum*1.0)/count
        

