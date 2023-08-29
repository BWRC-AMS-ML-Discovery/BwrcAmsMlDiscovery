from discovery_shared.rpc import Rpc
from example_server import flip_flop_sim


def test_types():
    print(flip_flop_sim)
    assert type(flip_flop_sim) == Rpc

    print(flip_flop_sim.func)
    assert type(flip_flop_sim.func) == type(lambda x: x)


def test_sim():
    """
    TODO Add test cases
    """

    inp = None
    out = flip_flop_sim(inp)
    print(out)


def test():
    test_types()
    test_sim()


if __name__ == "__main__":
    test()