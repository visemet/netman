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
        """

        # Initializes each device
        for device in self._devices:
            events = device.initialize()

            eventList = device.initialize()
            for event in events:
                heappush(self._event_queue, event)

    def start(self):
        """
        """

        self._initialize()
        
        # Loops through all events on the queue
        while not self._event_queue:
            event = heappop(self._event_queue)

            # TODO: spawned_events = handle(event)
            port = event.port()
            device = port.out_link.source()

            spawned_events = device.process(port)

            for spawned_event in spawned_events:
                heappush(self._event_queue, spawned_event)
