from dataclasses import dataclass

import hdl21 as h
import vlsirtools.spice as vsp
import sky130
import sitepdks as _
from hdl21.prefix import µ, f, MILLI

FIXME = None


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
    vin = h.Param(dtype=int, desc="Input Voltage (mV)")


@h.generator
def Tb(params: TbParams) -> h.Module:
    """# Sky130 Inverter Testbench"""

    @h.module
    class Tb:
        # The sole testbench port: VSS
        VSS = h.Port()
        # Internal signals: input, output, supple
        inp, out, VDD = h.Signals(3)
        # The DUT Inverter
        inv = Inv(params.inv)(inp=inp, out=out, VDD=VDD, VSS=VSS)
        # Stimulus Sources: VDD and VIN
        vdd = h.Vdc(dc=params.vdd * MILLI)(p=VDD, n=VSS)
        vin = h.Vdc(dc=params.vin * MILLI)(p=inp, n=VSS)
        # Load Cap
        cl = h.Cap(c=10 * f)(p=out, n=VSS)

    return Tb


def sim(params: TbParams) -> h.sim.SimResult:
    """ # Simulate a testbench with `TbParams`, returning its `SimResults` """

    @h.sim.sim
    class InvSim:
        """# Inverter Simulation Input"""

        # Testbench
        tb = Tb(params)

        # Stimulus
        op = h.sim.Op()
        # tran = h.sim.Tran(tstop=1*h.prefix.PICO)
        models = h.sim.Lib(path=sky130.install.model_lib, section="tt")

        # These painful settings for ngspice
        l1 = h.sim.Literal("set ngbehavior=hsa")
        l2 = h.sim.Literal("set ng_nomodcheck")

    sim_options = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE, rundir="./scratch/"
    )

    # Run the simulation!!
    return InvSim.run(sim_options)


@dataclass
class Result:
    """# Inverter DC Simulation(s) Result"""

    idsatp: float  # PMOS Id,sat
    idsatn: float  # NMOS Id,sat


def inverter(params: InvParams) -> Result:
    """# Inverter top-level entrypoint"""

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
# inverter(InvParams(wp=1 * µ, wn=1 * µ))
