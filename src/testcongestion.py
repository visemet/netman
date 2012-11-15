#!/usr/bin/env python

import flow
import congestion.aimd
from numpy import *
from pylab import *


N = 1000
Idx = arange(N)
W = zeros(N)
c1 = congestion.aimd.AIMD()
c1.initialize(1,4,50)
for i in arange(N-1) + 1:
    randnum = rand()
    if randnum > 0.01 :
        c1.handle_ack_received()
        W[i] = c1.cwnd()
    else :
        c1.handle_packet_dropped()        
        W[i] = c1.cwnd()    
plot(Idx, W)
xlabel('time')
ylabel('window size')
show()
