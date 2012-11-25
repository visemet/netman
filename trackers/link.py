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
        self._times_sent = []
        self._packetLosses = []
        self._bufferSize = [] # list of tuples of time,size
        
    def record_sent(self, time):
        """
            given the time a packet was sent, add it to the list
        """
        self._times_sent.append(time)
    
    def add_packet_loss(self, time, num=1):
        """
        records a packet loss at a given time
        """
        self._packetLosses.append(num, time)
        
    def record_buffer_size(self, time, size):
        """
            given the time and size, record as tuple in the list
        """
        self._bufferSize.append((time,size))

    #return list of (time, num) where num is the number of packets lost at
    # that moment in time
    def getPacketLossData():
        packetLossData ={}
        for num,time in self._packetLosses:
            if time in packetLossData.keys():
                packetLossData[time] += 1
            else:
                packetLossData[time] = 0
        returnValue = []
        for time,val in packetLossData:
            returnValue.append((time,val))
        return returnValue
    
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
        return returnValue
    
    #return list of (time, num) where num is the occupancy of the buffer at
    # that point in time
    def getBufferOccupancyData():
        return self._bufferSize
