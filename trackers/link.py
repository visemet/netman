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

        self._times_sent = [] # list of times

        self._packet_losses = [] # list of times

        self._buffer_sizes = [] # list of tuples (time, size)

        self._round_trips = [] # list of tuples (time, rtt)
        
    def record_sent(self, time):
        """
        Records the time when a packet is sent.
        """

        self._times_sent.append(time)
    
    def record_packet_loss(self, time):
        """
        Records the time when a packet is lost.
        """

        self._packet_losses.append(time)
        
    def record_buffer_size(self, time, size):
        """
        Records the buffer size at a certain time.
        """

        self._buffer_sizes.append((time,size))

    def record_round_trip(self, time, rtt):
        """
        Records the round trip time at a certain time.
        """

        self._round_trips.append((time, rtt))

    def average_rtt(self, since):
        """
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

    # return points in a form that simulation.generate_graph will accept
    #return list of (time, num) where num is the number of packets lost at
    # that moment in time
    def getPacketLossData():
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
    
    # return points in a form that simulation.generate_graph will accept
    # return list of (time, num) where num is the number of packets sent at that 
    #  time
    def getLinkRateData():
        linkRateData = {}     
        for t in self._times_sent:
            if t in linkRateData.keys():
                linkRateData[t] += 1
            else:
                linkRateData[t] = 1
                
        returnValue = []
        for time, value in linkRateData:
            returnValue.append((time,value))
        returnValue.sort() #sort by first value, which is time
        return returnValue
    
    #return list of (time, num) where num is the occupancy of the buffer at
    # that point in time
    def getBufferOccupancyData():
        return self._buffer_sizes
