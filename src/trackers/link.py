from device import Device

class LinkTracker:
    """
    Builder for LinkTracker instances.
    """

    def __init__(self):
        """
        Creates a new LinkTracker instance with 
            packetLosses initialized to 0
            empty timeTraces list
            
        """
        self._packetLosses = 0
        self._timeTraces = []
        #return self

    def addTrace(self, start, end):
        """
        adds a tuple of occupancy start and end dates
        """
        self._timeTraces.append((start, end))

    def addPacketLoss(self, num=1):
        """
        records a packet loss
        """
        self.packetLosses += num
