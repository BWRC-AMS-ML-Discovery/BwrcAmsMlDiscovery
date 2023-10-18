""" 
# Folded Cascode OpAmp
"""

from dataclasses import asdict
import hdl21 as h

from autockt_shared import FoldedCascodeInput, OpAmpOutput

# Local Imports
from ..pdk import nmos, pmos
from .tb import TbParams, simulate


@h.paramclass
class FoldedCascodeParams:
    """Parameter class"""

    w1_2 = h.Param(dtype=int, desc="Width of M1/2", default=10)
    w5_6 = h.Param(dtype=int, desc="Width of M5/6", default=10)
    w7_8 = h.Param(dtype=int, desc="Width of M7/8", default=10)
    w9_10 = h.Param(dtype=int, desc="width of M9/10", default=10)
    w11_12 = h.Param(dtype=int, desc="Width of M11/12", default=10)
    w13_14 = h.Param(dtype=int, desc="Width of M13/14", default=10)
    w15_16 = h.Param(dtype=int, desc="Width of M15/16", default=10)
    w17 = h.Param(dtype=int, desc="Width of M17", default=10)
    w18 = h.Param(dtype=int, desc="width of M18", default=10)

    cl = h.Param(dtype=h.Scalar, desc="cl capacitance", default=1e-14)
    cc = h.Param(dtype=h.Scalar, desc="cc capacitance", default=1e-14)
    rc = h.Param(dtype=h.Scalar, desc="rc resistor", default=100)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)

    wb0 = h.Param(dtype=int, desc="Width of MB0 ", default=10)
    wb1 = h.Param(dtype=int, desc="Width of MB1 ", default=10)
    wb2 = h.Param(dtype=int, desc="Width of MB2 ", default=10)
    wb3 = h.Param(dtype=int, desc="Width of MB3 ", default=10)
    wb4 = h.Param(dtype=int, desc="Width of MB4 ", default=10)
    wb5 = h.Param(dtype=int, desc="Width of MB5 ", default=10)
    wb6 = h.Param(dtype=int, desc="Width of MB6 ", default=10)
    wb7 = h.Param(dtype=int, desc="Width of MB7 ", default=10)
    wb8 = h.Param(dtype=int, desc="Width of MB8 ", default=10)
    wb9 = h.Param(dtype=int, desc="Width of MB9 ", default=10)
    wb10 = h.Param(dtype=int, desc="Width of MB10", default=10)
    wb11 = h.Param(dtype=int, desc="Width of MB11", default=10)
    wb12 = h.Param(dtype=int, desc="Width of MB12", default=10)
    wb13 = h.Param(dtype=int, desc="Width of MB13", default=10)
    wb14 = h.Param(dtype=int, desc="Width of MB14", default=10)
    wb15 = h.Param(dtype=int, desc="Width of MB15", default=10)
    wb16 = h.Param(dtype=int, desc="Width of MB16", default=10)
    wb17 = h.Param(dtype=int, desc="Width of MB17", default=10)
    wb18 = h.Param(dtype=int, desc="Width of MB18", default=10)
    wb19 = h.Param(dtype=int, desc="Width of MB19", default=10)

    ibias = h.Param(dtype=h.Scalar, desc="ibias current", default=30e-6)
    Vcm = h.Param(dtype=h.Scalar, desc="Vcm", default=1)


@h.generator
def Fcasc(params: FoldedCascodeParams) -> h.Module:
    """# Rail-to-Rail, Dual Input Pair, Folded Cascode, Diff to SE Op-Amp"""

    Nbias = lambda x: nmos(m=x)
    Ncasc = nmos()
    Pbias = lambda x: pmos(m=x)
    Pcasc = pmos()

    @h.module
    class Fcasc:
        # IO
        VDD, VSS = h.Ports(2)
        inp = h.Diff(port=True)
        out = h.Output()
        ibias1, ibias2 = h.Inputs(2)

        # Implementation
        outn = h.Signal()
        outd = h.bundlize(p=outn, n=out)
        psd = h.Diff()
        nsd = h.Diff()
        pcascg, pbias = h.Signals(2)

        ## Output Folded Stack
        ptop = h.Pair(Pbias(x=2))(g=outn, d=psd, s=VDD, b=VDD)
        pcasc = h.Pair(Pcasc)(g=pcascg, s=psd, d=outd, b=VDD)
        ncasc = h.Pair(Ncasc)(g=ibias2, s=nsd, d=outd, b=VSS)
        nbot = h.Pair(Nbias(x=2))(g=ibias1, d=nsd, s=VSS, b=VSS)

        ## Nmos Input Pair
        nin_bias = Nbias(x=2)(g=ibias1, s=VSS, b=VSS)
        nin = h.Pair(nmos(nser=1, npar=4))(g=inp, d=psd, s=nin_bias.d, b=VSS)

        ## Pmos Input Pair
        pin_bias = Pbias(x=2)(g=pbias, s=VDD, b=VDD)
        pin = h.Pair(pmos(nser=1, npar=4))(g=inp, d=nsd, s=pin_bias.d, b=VDD)

        ## Bias Tree
        ### Nmos Cascode Gate Generator, with series-nmos "resistor"
        ncdiode = nmos(nser=32)(g=ibias2, d=ibias2, s=VSS, b=VSS)

        ### Bottom Nmos Diode (with cascode)
        ndiode_casc = Ncasc(g=ibias2, d=ibias1, b=VSS)
        ndiode = Nbias(x=1)(g=ibias1, d=ndiode_casc.s, s=VSS, b=VSS)

        ### Nmos Mirror to pmos Cascode Bias
        n1casc = Ncasc(g=ibias2, d=pcascg, b=VSS)
        n1src = Nbias(x=1)(g=ibias1, d=n1casc.s, s=VSS, b=VSS)

        ### Pmos cascode bias, with magic voltage source
        pcdiode = pmos(nser=16)(g=pcascg, d=pcascg, s=VDD, b=VDD)

        ### Nmos Mirror to top pmos Bias
        n2casc = Ncasc(g=ibias2, d=pbias, b=VSS)
        n2src = Nbias(x=1)(g=ibias1, d=n2casc.s, s=VSS, b=VSS)

        ### Top Pmos Bias
        pdiode = Pbias(x=1)(g=pbias, s=VDD, b=VDD)
        pdiode_casc = Pcasc(s=pdiode.d, g=pcascg, d=pbias, b=VDD)

    return Fcasc


# def folded_cascode_sim(inp: FoldedCascodeInput) -> OpAmpOutput:
#     """
#     FoldedCascode Simulation
#     """
#     opts = vsp.SimOptions(
#         simulator=vsp.SupportedSimulators.NGSPICE,
#         fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
#         rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
#     )
#     if not vsp.ngspice.available():
#         print("ngspice is not available. Skipping simulation.")
#         return

#     params = FoldedCascodeParams(
#         w1_2=inp.w1_2,
#         w5_6=inp.w5_6,
#         w7_8=inp.w7_8,
#         w9_10=inp.w9_10,
#         w11_12=inp.w11_12,
#         w13_14=inp.w13_14,
#         w15_16=inp.w15_16,
#         w17=inp.w17,
#         w18=inp.w18,
#         # VDD=inp.VDD,
#         cl=inp.cl,
#         cc=inp.cc,
#         rc=inp.rc,
#         wb0=inp.wb0,
#         wb1=inp.wb1,
#         wb2=inp.wb2,
#         wb3=inp.wb3,
#         wb4=inp.wb4,
#         wb5=inp.wb5,
#         wb6=inp.wb6,
#         wb7=inp.wb7,
#         wb8=inp.wb8,
#         wb9=inp.wb9,
#         wb10=inp.wb10,
#         wb11=inp.wb11,
#         wb12=inp.wb12,
#         wb13=inp.wb13,
#         wb14=inp.wb14,
#         wb15=inp.wb15,
#         wb16=inp.wb16,
#         wb17=inp.wb17,
#         wb18=inp.wb18,
#         wb19=inp.wb19,
#         ibias=inp.ibias,
#         Vcm=inp.Vcm,
#     )


@h.generator
def FcascTb(params: TbParams) -> h.Module:
    """# FoldecCascode Op-Amp Testbench"""

    @h.module
    class OpAmpTb:
        VSS = h.Port()  # The testbench interface: sole port VSS

        # Drive VDD
        vdc = h.Vdc(dc=params.VDD)(n=VSS)
        inp = h.Diff()
        sig_out = h.Signal()
        sig_p = h.Vdc(dc=params.VDD / 2, ac=0.5)(p=inp.p, n=VSS)
        sig_n = h.Vdc(dc=params.VDD / 2, ac=-0.5)(p=inp.n, n=VSS)

        # Primary difference: the two bias current inputs
        ibias1, ibias2 = 2 * h.Signal()
        xibias1 = h.Isrc(dc=params.ibias)(p=vdc.p, n=ibias1)
        xibias1 = h.Isrc(dc=params.ibias)(p=vdc.p, n=ibias2)

        # The Op-Amp DUT
        inst = params.dut(
            VDD=vdc.p, VSS=VSS, ibias1=ibias1, ibias2=ibias2, inp=inp, out=sig_out
        )

    return OpAmpTb


def endpoint(inp: FoldedCascodeInput) -> OpAmpOutput:
    """# Folded Cascode OpAmp RPC Implementation"""

    # Convert `inp` into the generator's parameters
    # params = as_hdl21_paramclass(inp)

    VDD = h.prefix.Prefixed(number=1.2)
    ibias = h.prefix.Prefixed(number=3e-5)

    # Create a testbench, simulate it, and return the metrics!
    opamp = FoldedCascodeParams(**asdict(inp))
    tbparams = TbParams(
        dut=opamp,
        VDD=VDD,
        ibias=ibias,
    )
    tbmodule = FcascTb(tbparams)
    return simulate(tbmodule)
