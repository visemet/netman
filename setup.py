#!/usr/bin/python

from sys import argv

from buffer import Buffer
from congestion.aimd import AIMD
from conn import Link, Port
from flow import Flow
from host import Host
from router import Router
from routing.bellmanford import BellmanFord
from simulation import Simulation



class Setup:
    """
    # Hosts
    <name>

    # Routers
    <name, routing algorithm>

    # Connections
    <name, source, destination, link capacity, prop delay, buffer size>
        
    # Flows
    <name, source, destination, size, start time, congestion algorithm>

    # Measurables
    <name, type>
    """

    def __init__(self, filename):
        self._type_format = {'# Hosts':       0,
                             '# Routers':     1,
                             '# Connections': 2,
                             '# Flows':       3,
                             '# Measurables': 4}

        config = open(filename, 'r')
        (self.devices, self.flows, self.links) = self._initialize(config)

    def _initialize(self, config):
        curr_type = -1
        devices = {}
        links = {}
        flows = {}
        measure_flows = {}
        measure_links = {}

        for line in config:
            line = line.strip()

            if line in self._type_format:
                curr_type = self._type_format[line]
                continue
 
            # Hosts
            if curr_type == 0:
                [name] = line.split(', ')
                host = Host(name)
                devices[name] = host

            # Routers
            elif curr_type == 1:
                [name, algorithm] = line.split(', ')

                if algorithm == BellmanFord._TYPE:
                    algorithm = BellmanFord()

                router = Router(algorithm, name)
                devices[name] = router

            # Connections
            elif curr_type == 2:
                [name, source, dest, rate, delay, size] = line.split(', ')

                source_device = devices[source]
                dest_device = devices[dest]
                rate = int(rate)
                delay = float(delay)
                size = int(size)

                source_link = Link()
                dest_link = Link()

                source_port = Port()
                source_port.source(source_device)
                source_port.conn(dest_link)
                source_port.incoming(Buffer(size))
                source_port.outgoing(Buffer(size))

                dest_port = Port()
                dest_port.source(dest_device)
                dest_port.conn(source_link)
                dest_port.incoming(Buffer(size))
                dest_port.outgoing(Buffer(size))

                source_link.dest(source_port)
                source_link.rate(rate)
                source_link.delay(delay)
                source_link.getTracker().set_delay(delay)

                dest_link.dest(dest_port)
                dest_link.rate(rate)
                dest_link.delay(delay)
                dest_link.getTracker().set_delay(delay)

                source_device.enable(source_port)
                dest_device.enable(dest_port)
                
                links[name] = dest_link

            # Flows
            elif curr_type == 3:
                [name, source, dest, size, time, algorithm] = line.split(', ')

                source_device = devices[source]
                dest_device = devices[dest]
                size = int(size)
                time = float(time)

                congestion = AIMD()

                flow = Flow(congestion)
                flow.bits(size)
                flow.start(time)
                flow.dest(dest_device)

                congestion.initialize(flow)

                source_device.connect(flow)
                
                flows[name] = flow

            # Measurables
            elif curr_type == 4:
                # TODO: track measurables
                [name, type] = line.split(', ')
                if type == "flow":
                    measure_flows[name] = flows[name]
                elif type == "link":
                    measure_links[name] = links[name]

        return (devices.values(), measure_flows, measure_links)

if __name__ == '__main__':
    filename = argv[1]

    config = Setup(filename)
    devices = config.devices
    measure_flows = config.flows
    measure_links = config.links

    sim = Simulation(devices, measure_flows, measure_links)
    sim.start()
