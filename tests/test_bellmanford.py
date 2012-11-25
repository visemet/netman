import nose

from setup import Setup
from simulation import TestBellmanFord

def test_routing_less():
    filename = 'configs/routing-less.cfg'

    devices = Setup(filename).devices

    sim = TestBellmanFord(devices)
    sim.start()
