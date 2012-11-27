from heapq import heappush, heappop

from device import Device
from event import Event
from router import Router

import numpy
import matplotlib.pyplot as plt

class Simulation:
    """
    Class for running multi-link, multi-flow network simulations.
    """

    def __init__(self, devices):
        """
        Creates a Simulation instance with the specified list of
        devices.
        """

        # Checks that devices is a list
        if not isinstance(devices, list):
            raise TypeError, 'devices must be a list'

        # Iterates through each device
        for device in devices:
            # Checks that each device is a Device instance
            if not isinstance(device, Device):
                raise TypeError, 'device must be a Device instance'

        # Stores the list of devices
        self._devices = devices

        # Initializes an empty event queue
        self._event_queue = []

    def _initialize(self):
        """
        Initializes the simulation by initializing each device.
        """

        # Iterates through each device
        for device in self._devices:
            # Initializes each device
            events = device.initialize()

            # Pushes each event onto the queue
            for event in events:
                heappush(self._event_queue, event)

    def _finalize(self):
        """
        Finalizes the simulation.
        """

        pass

    def start(self):
        """
        Starts the simulation and executes it until completion.
        """

        # Initializes the simulation
        self._initialize()
        
        # Loops through all events on the queue
        while self._event_queue:
            # Pops the head off of the event queue
            event = heappop(self._event_queue)
            device = event.port().source()

            # Processes the event
            spawned_events = device.process(event)
            # Pushes each spawned event onto the queue
            for spawned_event in spawned_events:
                heappush(self._event_queue, spawned_event)

        # TODO: generate graphs from the statistics
        
        return self._finalize()
        
    '''
    @param
        points = list[] of (x,y) where x is the x-coordinate and y is the y-coordinate
            chose dictionary for purposes of aggregating data at a single point so it's
            easier for the data-collecting function--change?
        filename: ex. windowSize. 
        ytitle - technically we could just use the filename, but this allows us
            to specify units. xtitle is always going to be time
    
    File will be saved as <filename>.png
    
    '''
    def generate_graph(points, filename, ytitle):
        p = plt.figure()
        p.suptitle(filename)
        ax = p.add_subplot(111)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(ytitle)
        #graph the line between the previous point and the current point. 
        #Always start the previous point at the origin TODO: is this okay?
        #After every iteration, update the previous point to be the current point
        prevpoint = (0,0)
        for x,y in points:
            # plot x1,x2 y1,y2
            ax.plot([prevpoint[0], x], [prevpoint[1], y], 'r-')
            prevpoint = (x,y)
        p.savefig(filename + '.png')

class TestBellmanFord(Simulation):
    """
    Simulation that verifies the Bellman-Ford algorithm.
    """

    # Overrides Simulation._finalize()
    def _finalize(self):
        """
        Finalizes the simulation by returning the routing tables.
        """

        routing_tables = {}

        for device in self._devices:
            if isinstance(device, Router):
                routing_tables[device] = device._algorithm._routing_table

        return routing_tables
