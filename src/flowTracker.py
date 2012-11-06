from device import Device

class FlowTracker:
    """
    Builder for FlowTracker instances.
    """

    def __init__(self):
        """
        Creates a new FlowTracker instance with 
            packetsSent = []
            packetsReceived = []
            lists are lists of times at which the packet was sent or received
            
        """
        self._packetsSent = 0
        self._packetsReceived = 0
        return self

    def packetSent(self, time):
        """
        adds a time log of when a packet was sent
        """
        self._packetsSent.append(time)

    def numPacketsSent(self):
        '''
            return the total number of packets sent
        '''
        return len(self._packetsSent)
   
    def packetReceived(self, time):
        '''
        adds a time log of when a packet was received
        '''
        self._packetsReceived.add(time)
        
    def numPacketsReceived(self):
        '''
        return the total number of packets received
        '''
        return len(self._packetsReceived)
    
    def sendRate(self):
        '''
        return the send Rate
        '''
        return numPacketsSent()/  \
            (packetsSent[len(self._packetsSent)-1] - packetsSent[0]) #TODO should start time be 0?
                
    def receiveRate(self):
        '''
        return the receive rate
        '''
        return numPacketsReceived()/  \
            (packetsReceived[len(self._packetsReceived)-1] - packetsReceived[0]) # TODO should start time be 0?
            
    def packetDelay(self):
        '''
        return the average packet delay
        '''
        #TODO is this the average of the distance between corresponding send and receive times?
        packetDelay = 0
        return packetDelay