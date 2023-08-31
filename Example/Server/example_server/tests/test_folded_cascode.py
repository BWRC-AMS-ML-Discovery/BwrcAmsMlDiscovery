from discovery_shared.rpc import Rpc
from example_server import folded_cascode_sim


def test_types():
    print(folded_cascode_sim)
    assert type(folded_cascode_sim) == Rpc

    print(folded_cascode_sim.func)
    assert type(folded_cascode_sim.func) == type(lambda x: x)


def test_sim():
    """
    TODO Add test cases
    """

    inp = None
    out = folded_cascode_sim(inp)
    print(out)


def test():
    test_types()
    test_sim()


if __name__ == "__main__":
    test()
