from discovery_shared.rpc import Rpc
from example_server import latch_sim


def test_types():
    print(latch_sim)
    assert type(latch_sim) == Rpc

    print(latch_sim.func)
    assert type(latch_sim.func) == type(lambda x: x)


def test_sim():
    """
    TODO Add test cases
    """

    inp = None
    out = latch_sim(inp)
    print(out)


def test():
    test_types()
    test_sim()


if __name__ == "__main__":
    test()
