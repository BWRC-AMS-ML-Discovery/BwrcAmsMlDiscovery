from discovery_shared.rpc import Rpc
from eval_engines import folded_cascode_sim, FoldedCascodeInput


def test_types():
    print(folded_cascode_sim)
    assert type(folded_cascode_sim) == Rpc

    print(folded_cascode_sim.func)
    assert type(folded_cascode_sim.func) == type(lambda x: x)


def test_sim():
    """
    TODO Add test cases
    """
    inp = FoldedCascodeInput(
        w1_2=10,
        w5_6=10,
        w7_8=10,
        w9_10=10,
        w11_12=10,
        w13_14=10,
        w15_16=10,
        w17=10,
        w18=10,
        cl=10e-15,
        cc=10e-15,
        rc=1e3,
        wb0=10,
        wb1=10,
        wb2=10,
        wb3=10,
        wb4=10,
        wb5=10,
        wb6=10,
        wb7=10,
        wb8=10,
        wb9=10,
        wb10=10,
        wb11=10,
        wb12=10,
        wb13=10,
        wb14=10,
        wb15=10,
        wb16=10,
        wb17=10,
        wb18=10,
        wb19=10,
        ibias=40e-6,
        Vcm=1,
    )

    out = folded_cascode_sim(inp)
    print(out)


def test():
    test_types()
    test_sim()


if __name__ == "__main__":
    test()
