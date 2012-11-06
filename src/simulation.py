'''
receives the configuration from setup.py
initializes the devices
initializes the event queue
'''

import routing.static
import router
import port
import link
import host
import flow 

class Simulate:
    def __init__(self, devices):
        self._eventQueue = []
        # initialize the devices, receive the event back, put the event into the queue
        for device in devices:
            #TODO is the returned event an event or a list of events?
            eventList = device.initialize()
            for event in eventList:
                heappush(eventQueue, event)
        
        #start the loop
        while not empty(self._eventQueue):
            #handle the event, receive the new events spawned back from it
            newEvents = handle(heappop(self._eventQueue))
            for event in newEvents:
                heappush(eventQueue, event)
            
        print "terminated \n"
