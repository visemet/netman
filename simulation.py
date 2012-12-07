from heapq import heappush, heappop

from device import Device
from event import Event
from router import Router


from graph import Graph

class Simulation:
    """
    Class for running multi-link, multi-flow network simulations.
    """

    def __init__(self, devices, measure_flows, measure_links):
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
        
        self._measure_flows = measure_flows
        self._measure_links = measure_links

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
        # TODO: generate graphs from the statistics
        
        #flow-related graphs
        window_size_graph = Graph("window size", "cwnd (packet)")
        flow_rate_graph = Graph("flow rate", "send (Mbpms)")
        rtt_graph = Graph("round trip time", "time (ms)")
            #retrieve from flowtracker
        for flow_name in self._measure_flows.keys():
            f = self._measure_flows[flow_name].getTracker()
            #window size graph
            window_size_graph.add_data_set(flow_name, f.get_window_size_data())
            #flow rate graph
            flow_rate_graph.add_data_set(flow_name, f.get_flow_rate_data())
            #rtt graph
            rtt_graph.add_data_set(flow_name, f.get_rtt_data())
        
        #link-related graphs
        buffer_occupancy_graph = Graph("buffer occupancy", "buffer (packet)")
        packet_loss_graph = Graph("packet loss", "losses (packets)")
        link_rate_graph = Graph("link rate", "link rate (Mbpms)")
        
        for link_name in self._measure_links.keys():
            l = self._measure_links[link_name].getTracker()
            l.set_delay(self._measure_links[link_name].delay())
            #buffer occupancy graph
            buffer_occupancy_graph.add_data_set(link_name, l.get_buffer_occupancy_data())
            #packet loss graph
            packet_loss_graph.add_data_set(link_name, l.get_packet_loss_data())
            #link rate graph
            link_rate_graph.add_data_set(link_name, l.get_link_rate_data())

        window_size_graph.generate_total_graph()
        flow_rate_graph.generate_total_graph()
        buffer_occupancy_graph.generate_total_graph()
        packet_loss_graph.generate_total_graph()
        link_rate_graph.generate_total_graph()
        rtt_graph.generate_total_graph()
        

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

        return self._finalize()

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
