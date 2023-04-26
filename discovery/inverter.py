from dataclasses import dataclass
from textwrap import dedent

import hdl21 as h
from hdl21.prefix import MILLI
import vlsirtools.spice as vsp
import sky130
import sitepdks as _


@h.paramclass
class InvParams:
    """# Inverter Parameters"""

    wp = h.Param(dtype=int, desc="PMOS Width (nm)")
    wn = h.Param(dtype=int, desc="NMOS Width (nm)")


@h.generator
def Inv(params: InvParams) -> h.Module:
    """# Sky130 Inverter"""

    # Apply our size parameters
    # Reminder: our `InvParams` are integer *nanometers*, and the Sky PDK wants *microns*!
    nfet = sky130.modules.sky130_fd_pr__nfet_01v8(w=params.wn * MILLI)
    pfet = sky130.modules.sky130_fd_pr__pfet_01v8(w=params.wp * MILLI)

    @h.module
    class Inv:
        inp, VDD, VSS = h.Inputs(3)
        out = h.Output()
        p = pfet(d=out, g=inp, s=VDD, b=VDD)
        n = nfet(d=out, g=inp, s=VSS, b=VSS)

    return Inv


@h.paramclass
class TbParams:
    """# TestBench Parameters"""

    inv = h.Param(dtype=InvParams, desc="Inverter Parameters")
    vdd = h.Param(dtype=int, desc="Supply Voltage (mV)")
    inp = h.Param(dtype=bool, desc="Input Logic Level (Boolean)")


@h.generator
def Tb(params: TbParams) -> h.Module:
    """# Sky130 Inverter Id,sat Testbench"""

    # Extract voltages for stimulus sources
    vvdd = params.vdd * MILLI # Convert to volts
    vvin = vvdd if params.inp else 0

    @h.module
    class Tb:
        # The sole testbench port: VSS
        VSS = h.Port()
        # Internal signals: input/output, supply
        io, VDD = h.Signals(2)
        
        # The DUT Inverter
        inv = Inv(params.inv)(inp=io, out=io, VDD=VDD, VSS=VSS)
        
        # Stimulus Sources: VDD, VIN, VOUT
        vdd = h.Vdc(dc=vvdd)(p=VDD, n=VSS)
        vio = h.Vdc(dc=vvin)(p=io, n=VSS)

    return Tb


def sim(params: TbParams) -> h.sim.SimResult:
    """# Simulate a testbench with `TbParams`, returning its `SimResults`"""

    @h.sim.sim
    class InvSim:
        """# Inverter Simulation Input"""

        # These painful settings for ngspice
        ng = h.sim.Literal(
            dedent(
                """
            .control
            set ngbehavior=hsa
            set ng_nomodcheck
            .endc
        """
            )
        )
        # Sky130 Model Library
        models = h.sim.Lib(path=sky130.install.model_lib, section="tt")

        # Testbench
        tb = Tb(params)

        # Stimulus
        op = h.sim.Op()
        ## FIXME: after id,sat sims and tests work, add some transient!
        # tran = h.sim.Tran(tstop=1*h.prefix.PICO)

    sim_options = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE, 
        fmt=vsp.ResultFormat.SIM_DATA, #
        rundir="./scratch/"
    )

    # Run the simulation!!
    return InvSim.run(sim_options)


@dataclass
class Result:
    """# Inverter DC Simulation(s) Result"""

    idsatp: float  # PMOS Id,sat
    idsatn: float  # NMOS Id,sat


def inverter(params: InvParams) -> Result:
    """
    # Inverter top-level entrypoint
    FIXME TODO: this is the primary thing to write and do! 
    And then hook it up to the stuff in `server`. 
    """

    # Run the nmos-on sim
    result0 = sim(SomeValueOfParams())
    # Extract its id,sat
    idsatn = something(result0)

    # Run the pmos-on sim
    result1 = sim(SomeValueOtherParams())
    # Extract its id,sat
    idsatp = something(result1)

    return Result(
        idsatp=idsatp,
        idsatn=idsatn,
    )


# Test run (remove me plz!)
# inverter(InvParams(wp=1000, wn=1000))
params = TbParams(inv=InvParams(wp=1000, wn=1000), vdd=1800, inp=False)
print(f"`sim`'ing {params}")
res = sim(params)
print(res)
