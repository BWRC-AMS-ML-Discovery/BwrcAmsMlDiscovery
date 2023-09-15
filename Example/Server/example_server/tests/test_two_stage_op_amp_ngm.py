from discovery_shared.rpc import Rpc
from example_server import (
    two_stage_op_amp_ngm_sim,
    TwoStageOpAmpNgmInput,
    TwoStageOpAmpNgmOutput,
)


def test_types():
    print(two_stage_op_amp_ngm_sim)
    assert type(two_stage_op_amp_ngm_sim) == Rpc

    print(two_stage_op_amp_ngm_sim.func)
    assert type(two_stage_op_amp_ngm_sim.func) == type(lambda x: x)


def test_sim():
    """
    TODO Add test cases
    """

    inp = TwoStageOpAmpNgmInput(
        wtail1=10,
        wtail2=10,
        wcm=10,
        win=10,
        wref=10,
        wd1=10,
        wd=10,
        wn_gm=10,
        wtail=10,
        wtailr=10,
        Cc=100e-15,
        Rf=1e3,
        VDD=1.2,
        Vcm=1,
        Vref=1,
        ibias=2e-6,
    )
    out = two_stage_op_amp_ngm_sim(inp)
    print(out)


def test():
    test_types()
    test_sim()


if __name__ == "__main__":
    test()
