from device import Device

class LinkTracker:
    """
    Builder for LinkTracker instances.
    """

    def __init__(self):
        """
        Creates a new LinkTracker instance with 
            packetLosses initialized to 0
            empty times_sent list
            
        """
        self._times_sent = [] # list of tuples (time, size)

        self._packet_losses = [] # list of times

        self._buffer_sizes = [] # list of tuples (time, size)

        self._round_trips = [] # list of tuples (time, rtt)
        
<<<<<<< HEAD
        self._link_rates = []

        self._delay = 0

    def set_delay(self, delay):
        self._delay = delay
    
=======
>>>>>>> ace7cc8a6a9d2df2723ffc40379661772ac3a0c6
    def record_sent(self, time, size):
        """
        Records the time when a packet is sent.
        """
        #print "tracker" + str(time) + " " + str(size)
        self._times_sent.append((time, size))
        #print "len" + str(len(self._times_sent))

    def record_packet_loss(self, time):
        """
        Records the time when a packet is lost.
        """

        self._packet_losses.append(time)
        
    def record_buffer_size(self, time, size):
        """
        Records the buffer size at a certain time.
        """

        self._buffer_sizes.append((time, size))
        
    def record_linkrate(self, time, rate):
        '''
        record the link throughput at a certain time
        '''
        self._link_rates.append((time, rate))

    def record_round_trip(self, time, rtt):
        """
        Records the round trip time at a certain time.
        """

        self._round_trips.append((time, rtt))

    def occupancy(self, since, until, delay):
        """
        Returns the number of packets in the link between the specified
        times.
        """

        total_size = 0

        for time, size in self._times_sent:
            if since < (time + delay) and until > time:
                initial = max(time, since)
                final = min(time + delay, until)

                part = float(final - initial) / float(delay)

                total_size += size * part

        return total_size

    def num_losses(self, since, until):
        """
        Returns the number of losses in the link between the specified
        times.
        """

        num_losses = 0

        for time in self._packet_losses:
            if since <= time <= until:
                num_losses += 1

        return num_losses

    def mean_rtt(self, since):
        """
        Returns the average round trip time since the specified time.
        """

        sum_rtt = 0
        count_rtt = 0

        for (time, rtt) in reversed(self._round_trips):
            if time < since:
                break

            sum_rtt += rtt
            count_rtt += 1

        if count_rtt == 0:
            return -1

        return (float(sum_rtt) / float(count_rtt))

    def variance_rtt(self, since):
        """
        Returns the variance in the round trip time since the specified
        time.
        """

        sum_square_deviations = 0
        count_square_deviations = 0

        mean_rtt = self.mean_rtt(since)

        for (time, rtt) in reversed(self._round_trips):
            if time < since:
                break

            sum_square_deviations += (rtt - mean_rtt) ** 2
            count_square_deviations += 1

        if count_square_deviations == 0:
            return 0

        return (float(sum_square_deviations) / float(count_square_deviations))

    def throughput(self, since, until):
        """
        Returns the throughput of the link within the given time range.
        """

        occupancy = self.occupancy(since, until, self._delay)

        if (until - since) == 0:
            return 0
        else:
            return (float(occupancy) / float(until - since))
            
    # return points in a form that simulation.generate_graph will accept
    #return list of (time, num) where num is the number of packets lost at
    # that moment in time
    def get_packet_loss_data(self):
        packetLossData ={}
        for num,time in self._packet_losses:
            if time in packetLossData.keys():
                packetLossData[time] += 1
            else:
                packetLossData[time] = 0
        returnValue = []
        for time,val in packetLossData:
            returnValue.append((time,val))
        returnValue.sort() #sort by first value, which is time
        return returnValue

    def get_sent_times(self):
        return self._times_sent

    def get_previous_linkrate_point(self):
        if len(self._link_rates) < 2:
            return 0
        else:
            return self._link_rates[len(self._link_rates) -2][0]
            
    def get_link_rate_data(self):
        self._times_sent.sort()
        returnValue = []
        prev = 0
        i = 1

        while i < len(self._times_sent):
            rate = self.throughput(self._times_sent[prev][0], self._times_sent[i][0])
            returnValue.append((self._times_sent[i][0], rate))
            prev += 1
            i += 1
        return returnValue
        #return [(0,0), (1,0)]
        #return self._link_rates
        
    #return list of (time, num) where num is the occupancy of the buffer at
    # that point in time
    def get_buffer_occupancy_data(self):
        prev = 0
        i = 1
        self._buffer_sizes.sort()
        returnValue = []
        while i < len(self._buffer_sizes):
            occ = self.occupancy(self._buffer_sizes[prev][0], self._buffer_sizes[i][0], self._delay)
            returnValue.append((self._buffer_sizes[i][0], occ))
            prev += 1
            i += 1
        return returnValue

        return self._buffer_sizes
