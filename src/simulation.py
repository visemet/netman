from heapq import heappush, heappop

from device import Device
from event import Event

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

        for device in self._devices:
            print (device, device._algorithm._routing_table)
