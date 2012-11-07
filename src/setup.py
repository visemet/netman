#!/usr/bin/python

'''
This class reads in the inputs and creates the devices and connections

Expects an input file with the inputs in the following order:
#Source Hosts 
<one host per line>
#Destination Hosts
<one host per line>
#Routers
<one router per line>
#Links
<one link specification per line>
<end1, end2, capacity, delay, buffer size>
#Flows
<one flow specification per line>
<source, destination, size, start time, routing algorithm, congestion control>
#Measureables  #TODO


 '''

from collections import deque
import sys

from flow import Flow
from host import Host
from link import Link
from port import Port
from router import Router
from routing.bellmanford import BellmanFord
from simulation import Simulation

if __name__ == '__main__':
    # read index file to determine device types
    #indexfile = open(raw_input('Enter index file\n'))
    #matrixfile = open(raw_input('Enter matrix file\n'))
    
    inputType = -1
    '''
    defines the type of classes that we are currently looking at
    0 = hosts
    1 = routers
    2 = links
    3 = flows
    4 = links to measure #TODO
    5 = flows to measure #TODO
    '''
    
    filename = sys.argv[1]
    config = open(filename, 'r')

    devices = {}
    for line in config:
        if line[0] == '#':      # skip commented lines
            inputType += 1
            continue    
        if inputType == 0:      # source host
            newhost = Host(line.rstrip('\n'))
            devices[line.rstrip('\n')] = newhost
            print "host " + line.rstrip('\n')
        elif inputType == 1:
            algorithm = BellmanFord()
            newrouter = Router(algorithm, line.rstrip('\n'))
            devices[line.rstrip('\n')] = newrouter
            print "router " + str(line.rstrip('\n'))
        elif inputType == 2:
            info = line.rstrip('\n').split(' ')
            #create a link of the appropriate size between the two devices
            #create the link going the other direction as well
            link1 = Link().initTracker()
            link2 = Link().initTracker()

            newport = Port().device(devices[info[0]]).in_link(link1).out_link(link2).in_queue(deque()).out_queue(deque())
            newport2 = Port().device(devices[info[1]]).in_link(link2).out_link(link1).in_queue(deque()).out_queue(deque())

            link1.source(newport2).destination(newport).rate(float(info[2])).delay(float(info[3]))
            print "link src: " + str(info[0]) + " dest:" + str(info[1]) + " rate:" + str(info[2])
            link2.source(newport).destination(newport2).rate(float(info[2])).delay(float(info[3]))
            print "link src: " + str(info[1]) + " dest:" + str(info[0]) + " rate:" + str(info[2])

            print "port between links " + str(info[0]) + " " + str(info[1])
            print "port between links "+ str(info[1]) + " " + str(info[0])

            devices[info[0]].enable(newport)
            devices[info[1]].enable(newport2)

        elif inputType == 3:
            info = line.rstrip('\n').split(' ')
            #TODO: congestion algorithm
            #flow.Flow(int(info[2]), float(info[3]), devices[info[1]], None)
            print "flow destination: " + str(info[1]) + " bits: " + str(info[2]) \
                + " start time: " + str(info[3])
        elif inputType == 4:
            info = line.rstrip('\n').split(' ')
        elif inputType == 5:
            info = line.rstrip('\n').split(' ')
        else:
            print "Error - unrecognized input"
            exit()

    sim = Simulation(devices.values())
    sim.start()
            
    # begin the simulation with the setup devices
    #simulation.Simulate(devices)
'''    
a1 = routing.static.Static()
a2 = routing.static.Static()
a3 = routing.static.Static()

r1 = router.Router(a1)
r2 = router.Router(a2)
r3 = router.Router(a3)

l12 = link.Link().source(r1).destination(r2)
l13 = link.Link().source(r1).destination(r3)
l21 = link.Link().source(r2).destination(r1)
l23 = link.Link().source(r2).destination(r3)
l31 = link.Link().source(r3).destination(r1)
l32 = link.Link().source(r3).destination(r2)

p12 = port.Port().in_link(l21).out_link(l12)
p13 = port.Port().in_link(l31).out_link(l13)
p21 = port.Port().in_link(l12).out_link(l21)
p23 = port.Port().in_link(l32).out_link(l23)
p31 = port.Port().in_link(l13).out_link(l31)
p32 = port.Port().in_link(l23).out_link(l32)

r1.enable(p12)
r1.enable(p13)
r2.enable(p21)
r2.enable(p23)
r3.enable(p31)
r3.enable(p32)

r1.initialize()
r2.initialize()
r3.initialize()
'''
