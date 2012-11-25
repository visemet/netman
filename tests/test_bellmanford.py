import nose

from setup import Setup
from simulation import TestBellmanFord

def test_routing_less():
    filename = 'configs/routing-less.cfg'

    devices = Setup(filename).devices

    R1 = None
    R2 = None
    R3 = None
    R4 = None

    for device in devices:
        if device._id == 'R1':
            R1 = device
        elif device._id == 'R2':
            R2 = device
        elif device._id == 'R3':
            R3 = device
        elif device._id == 'R4':
            R4 = device

    sim = TestBellmanFord(devices)
    routing_tables = sim.start()

    assert routing_tables[R1][R2].conn().dest().source() == R2
    assert routing_tables[R1][R3].conn().dest().source() == R4
    assert routing_tables[R1][R4].conn().dest().source() == R4

    assert routing_tables[R2][R1].conn().dest().source() == R1
    assert routing_tables[R2][R3].conn().dest().source() == R1
    assert routing_tables[R2][R4].conn().dest().source() == R1

    assert routing_tables[R3][R1].conn().dest().source() == R4
    assert routing_tables[R3][R2].conn().dest().source() == R4
    assert routing_tables[R3][R4].conn().dest().source() == R4

    assert routing_tables[R4][R1].conn().dest().source() == R1
    assert routing_tables[R4][R2].conn().dest().source() == R1
    assert routing_tables[R4][R3].conn().dest().source() == R3
