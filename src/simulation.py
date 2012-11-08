from device import Device
from event import Event
from heapq import heappush, heappop

class Simulation:
    """
    """

    def __init__(self, devices):
        """
        Creates a simulation instance with the specified list of
        devices.
        """

        # TODO: check devices is list of Device instances
        self._devices = devices

        self._event_queue = []

    def _initialize(self):
        """
        Initializes the simulation.
        """

        # Iterates through each device
        for device in self._devices:
            # Initializes each device
            events = device.initialize()

            for event in events:
                heappush(self._event_queue, event)

    def start(self):
        """
        Starts the simulation.
        """

        # Initializes the simulation
        self._initialize()
        
        # Loops through all events on the queue
        while self._event_queue:
            # Removes the event from the head of the buffer
            event = heappop(self._event_queue)
            device = event.port().device()

            # Processes the event
            spawned_events = device.process(event)
            # Adds the spawned event to the queue
            for spawned_event in spawned_events:
                heappush(self._event_queue, spawned_event)

        for device in self._devices:
            print (device, device._algorithm._routing_table)
