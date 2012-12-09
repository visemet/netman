from device import Device
from math import floor

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

        self._link_rates = []

        self._delay = 0
        
        # the current queueing delay
        self._queueing_delay = 0
        
        self._queueing_delays= [] # stats for all packet delays
        self._packet_entries = {} # track packet:insert time

    def set_delay(self, delay):
        self._delay = delay

    #record that a packet has entered the buffer
    def record_packet_entry(self, packet, time):
        self._packet_entries[packet] = time
        
    #get the time that a packet entered the buffer
    def get_packet_entry(self, packet):
        return self._packet_entries[packet]

    #get the difference between entry and exit time for a packet in the buffer
    def update_queueing_delay(self, packet, time):
        val = time - self.get_packet_entry(packet)
        #update the current queueing delay
        self._queueing_delay = val
        
        #add the new statistics
        self._queueing_delays.append((time, val))
        
    def get_queueing_delay(self):
        return self._queueing_delay
    
    def get_average_queueing_delay(self, since):
        total_delay = 0
        count = 0

        for (time, delay) in reversed(self._queueing_delays):
            if time < since:
                break

            total_delay += delay
            count += 1

        if count == 0:
            return 0

        return (float(total_delay) / float(count))

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

    def occupancy(self, since, until, by, delay):
        """
        Returns the number of packets in the link at the specified
        time.
        """

        total_size = 0

        index = 0
        length = len(self._times_sent)

        go_back = -1

        while index < length:
            (time, size) = self._times_sent[index]

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

    def throughput(self, since, until, by):
        """
        Returns the throughput of the link within the given time range.
        """

        if (until - since) == 0:
            yield 0
        else:
            for occupancy in self.occupancy(since, until, by, self._delay):
                yield (float(occupancy) / float(by))

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
        """
        Returns the link rate data.
        """

        since = 0
        until = self._times_sent[-1][0] # (time, size)
        by = 1

        result = []

        for throughput in self.throughput(since, until, by):
            result.append((since + by, throughput))
            since += by

          
        everySecond = []
        currVal = 0
        currTime = 0
        for time, size in result:
            if (time / 250) == currTime:
                currVal = max(currVal, size)
            else:
                everySecond.append((currTime, currVal))
                currTime = (time / 250)   
                currVal = size
            
        return everySecond
        
        '''
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
        '''
        '''
        everySecond = []
        currCount = 0
        for time, size in result:
            if (currCount % 100)==0:
                everySecond.append((time, size))
            currCount += 1
        return everySecond
        '''

    #return list of (time, num) where num is the occupancy of the buffer at
    # that point in time
    def get_buffer_occupancy_data(self):
        returnValue = []
        temp = {}
        currTime = 0
        currSize = 0
        for time,size in self._buffer_sizes:
            if int(floor(time))==currTime:
                currSize = max(currSize, size)
            else:
                returnValue.append((currTime, currSize))
                currTime = int(floor(time))
                currSize = size
        returnValue.append((currTime, currSize))
        
        everySecond = []
        currVal = 0
        currTime = 0
        for time, size in returnValue:
            if (time / 250) == currTime:
                currVal = max(currVal, size)
            else:
                everySecond.append((currTime, currVal))
                currTime = (time / 250)   
                currVal = size
        return everySecond

        '''
        everySecond = []
        currVal = 0
        currTime = 0
        currSum = 0
        currCount = 0
        for time, size in returnValue:
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
        for time, size in returnValue:
            if (currCount % 100)==0:
                everySecond.append((time, size))
            currCount += 1
        return everySecond
        '''   

