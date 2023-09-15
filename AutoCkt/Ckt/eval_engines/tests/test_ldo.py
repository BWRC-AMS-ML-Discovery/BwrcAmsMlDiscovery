from discovery_shared.rpc import Rpc
from eval_engines import ldo_sim


def test_types():
    print(ldo_sim)
    assert type(ldo_sim) == Rpc

    print(ldo_sim.func)
    assert type(ldo_sim.func) == type(lambda x: x)


def test_sim():
    """
    TODO Add test cases
    """

    inp = None
    out = ldo_sim(inp)
    print(out)


def test():
    test_types()
    test_sim()


if __name__ == "__main__":
    test()
