from discovery_shared.rpc import Rpc
from eval_engines import latch_sim, LatchInput


def test_types():
    print(latch_sim)
    assert type(latch_sim) == Rpc

    print(latch_sim.func)
    assert type(latch_sim.func) == type(lambda x: x)


def test_sim():
    """
    TODO Add test cases
    """

    inp = LatchInput(
        w1=10, w2=20, w3=10, w4=20, w5=10, w6=20, w7=20, w8=20, w9=10, w10=10, VDD=1.2
    )
    out = latch_sim(inp)
    print(out)


def test():
    test_types()
    test_sim()


if __name__ == "__main__":
    test()
