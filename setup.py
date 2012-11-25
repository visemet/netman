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
    <source, destination, link capacity, prop delay, buffer size>

    # Flows
    <source, destination, size, start time, congestion algorithm>

    # Measurables
    <source, destination, type>
    """

    def __init__(self, filename):
        self._type_format = {'# Hosts':       0,
                             '# Routers':     1,
                             '# Connections': 2,
                             '# Flows':       3,
                             '# Measurables': 4}

        config = open(filename, 'r')
        self.devices = self._initialize(config)

    def _initialize(self, config):
        curr_type = -1
        devices = {}

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
                [source, dest, rate, delay, size] = line.split(', ')

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

                dest_link.dest(dest_port)
                dest_link.rate(rate)
                dest_link.delay(delay)

                source_device.enable(source_port)
                dest_device.enable(dest_port)

            # Flows
            elif curr_type == 3:
                [source, dest, size, time, algorithm] = line.split(', ')

                source_device = devices[source]
                dest_device = devices[dest]
                size = int(size)
                time = float(time)

                flow = Flow(AIMD())
                flow.bits(size)
                flow.start(time)
                flow.dest(dest_device)

                source_device.connect(flow)

            # Measurables
            elif curr_type == 4:
                # TODO: track measurables
                pass

        return devices.values()

if __name__ == '__main__':
    filename = argv[1]

    devices = Setup(filename).devices

    sim = Simulation(devices)
    sim.start()
