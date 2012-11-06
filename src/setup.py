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
import routing.static
import router
import port
import link
import host
import flow 
import simulation

if __name__=="__main__":
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
    
    inputfile = open("configs/test.cfg")
    devices = {}
    for line in inputfile:
        if line[0] == '#':      # skip commented lines
            inputType += 1
            continue    
        if inputType == 0:      # source host
            a1 = routing.static.Static() #TODO: non-static algorithm
            newhost = host.Host(a1)
            devices[str(line.rstrip('\n'))] = newhost
            print "host " + str(line.rstrip('\n'))
        elif inputType == 1:
            a1 = routing.static.Static() #TODO: non-static algorithm
            newrouter = router.Router(a1)
            devices[str(line.rstrip('\n'))] = newrouter
            print "router " + str(line.rstrip('\n'))
        elif inputType == 2:
            info = line.rstrip('\n').split(' ')
            #create a link of the appropriate size between the two devices
            #create the link going the other direction as well
            link1 = link.Link().initTracker().source(devices[str(info[0])]).destination(devices[info[1]]).rate(float(info[2]))
            print "link src: " + str(info[0]) + " dest:" + str(info[1]) + " rate:" + str(info[2])
            link2 = link.Link().initTracker().source(devices[info[1]]).destination(devices[info[0]]).rate(float(info[2]))
            print "link src: " + str(info[1]) + " dest:" + str(info[0]) + " rate:" + str(info[2])
            newport = port.Port().in_link(link1).out_link(link2)
            print "port between links"
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
    simulate()
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