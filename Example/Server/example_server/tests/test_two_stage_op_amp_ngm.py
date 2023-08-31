from discovery_shared.rpc import Rpc
from example_server import two_stage_op_amp_ngm_sim


def test_types():
    print(two_stage_op_amp_ngm_sim)
    assert type(two_stage_op_amp_ngm_sim) == Rpc

    print(two_stage_op_amp_ngm_sim.func)
    assert type(two_stage_op_amp_ngm_sim.func) == type(lambda x: x)


def test_sim():
    """
    TODO Add test cases
    """

    inp = None
    out = two_stage_op_amp_ngm_sim(inp)
    print(out)


def test():
    test_types()
    test_sim()


if __name__ == "__main__":
    test()
