# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
from dotenv import dotenv_values

# Workspace Imports
from example_shared import (
    example,
    Example,
    inverter_beta_ratio,
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
    auto_ckt_sim,
    auto_ckt_sim_hdl21,
    AutoCktInput,
    AutoCktOutput,
)

# The client library will create client stubs for all defined RPCs, including all those functions above.
import discovery_client as dc
from discovery_client import Config


def example_client_start(cfg: Config):
    """retrieve values from .env file then configure nad start the client"""

    dc.configure(cfg)

    if cfg.enable_https:
        dc.client_start()
    else:
        # Short-circuiting by directly calling server functions
        import example_server as _


"""
Now we can just call the RPCs as though they were implemented locally.
"""


def test_auto_ckt():
    """testing auto ckt rpcs"""
    to_test = AutoCktInput(3, 3, 3, 3, 3, 3, 1e-12)
    test = auto_ckt_sim(to_test)
    return test


def do_simple_example():
    example_resp = example(Example(txt="Hello", num=3))
    return example_resp


def local_inverter_beta_ratio(inp: InverterBetaRatioInput):
    wp = inp.wp
    wn = inp.wn
    output = (wp - 23) ** 2 + (wn - 4) ** 2
    return InverterBetaRatioOutput(
        trise=output / 2,
        tfall=output / 2,
    )
