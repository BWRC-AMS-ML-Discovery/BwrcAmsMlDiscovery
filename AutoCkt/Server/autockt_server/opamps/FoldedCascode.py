""" 
# Folded Cascode OpAmp
"""

from dataclasses import asdict
import hdl21 as h
from hdl21.prefix import FEMTO, MILLI, MICRO
from autockt_shared import FoldedCascodeInput, OpAmpOutput

# Local Imports
from ..typing import Hdl21Paramclass
from ..pdk import nmos, pmos
from .tb import TbParams, simulate


@h.generator
def Fcasc(params: Hdl21Paramclass(FoldedCascodeInput)) -> h.Module:
    """# Rail-to-Rail, Dual Input Pair, Folded Cascode, Diff to SE Op-Amp"""

    # Multiplier functions of the parametric devices
    nbias = lambda x: nmos(m=params.nbias * x)
    ncasc = lambda x: nmos(m=params.ncasc * x)
    ninp = lambda x: nmos(m=params.ninp * x)
    pbias = lambda x: pmos(m=params.pbias * x)
    pcasc = lambda x: pmos(m=params.pcasc * x)
    pinp = lambda x: pmos(m=params.pinp * x)

    # Give these some shorter-hands
    alpha, beta, gamma = params.alpha, params.beta, params.gamma

    @h.module
    class Fcasc:
        # IO Interface
        VDD, VSS = h.PowerGround()
        inp = h.Diff(port=True, role=h.Diff.Roles.SINK)
        out = h.Output()  # Single ended output
        ibias1, ibias2 = 2 * h.Input()

        # Implementation
        ## Internal Signals
        outn = h.Signal()
        outd = h.bundlize(p=outn, n=out)
        psd = h.Diff()
        nsd = h.Diff()
        pcascg, pbiasg = h.Signals(2)

        ## ###########################################################################
        ## Output Stack
        ## ###########################################################################
        ## Cascodes have current `gamma`
        ## Top has current `gamma + beta`
        ## Bottom has current `gamma + alpha`
        ## ###########################################################################
        pbo = h.Pair(pbias(x=gamma + beta))(g=outn, d=psd, s=VDD, b=VDD)
        pco = h.Pair(pcasc(x=gamma))(g=pcascg, s=psd, d=outd, b=VDD)
        nco = h.Pair(ncasc(x=gamma))(g=ibias2, s=nsd, d=outd, b=VSS)
        nbo = h.Pair(nbias(x=gamma + alpha))(g=ibias1, d=nsd, s=VSS, b=VSS)

        ## ###########################################################################
        ## Input Pairs
        ## Nmos has current `alpha` per leg, `2*alpha` in the bias devices
        ## Pmos has current `beta` per leg, `2*beta` in the bias devices
        ## ###########################################################################
        ##
        ## Nmos Input Pair
        nin_bias = nbias(x=2 * alpha)(g=ibias1, s=VSS, b=VSS)
        nin_casc = ncasc(x=2 * alpha)(g=ibias2, s=nin_bias.d, b=VSS)
        nin = h.Pair(ninp(x=alpha))(g=inp, d=psd, s=nin_casc.d, b=VSS)
        ##
        ## Pmos Input Pair
        pin_bias = pbias(x=2 * beta)(g=pbiasg, s=VDD, b=VDD)
        pin_casc = pbias(x=2 * beta)(g=pbiasg, s=pin_bias.d, b=VDD)
        pin = h.Pair(pinp(x=beta))(g=inp, d=nsd, s=pin_casc.d, b=VDD)

        ## ###########################################################################
        ## Bias Section
        ## ###########################################################################
        ## Everything in here is current-ratio one, i.e. all branches have `i=ibias`.
        ## Note every value of `x` equals one.
        ## ###########################################################################

        ### Nmos Cascode Gate Generator
        vcbn = h.Vdc(dc=params.vcb * MILLI)(n=VSS)
        ncdiode = ncasc(x=1)(g=ibias2, d=ibias2, s=vcbn.p, b=VSS)

        ### Bottom Nmos Diode (with cascode)
        ndiode_casc = ncasc(x=1)(g=ibias2, d=ibias1, b=VSS)
        ndiode = nbias(x=1)(g=ibias1, d=ndiode_casc.s, s=VSS, b=VSS)

        ### Nmos Mirror to pmos Cascode Bias
        n1casc = ncasc(x=1)(g=ibias2, d=pcascg, b=VSS)
        n1src = nbias(x=1)(g=ibias1, d=n1casc.s, s=VSS, b=VSS)

        ### Pmos cascode gate generator
        vcbp = h.Vdc(dc=params.vcb * MILLI)(p=VDD)
        pcdiode = pcasc(x=1)(g=pcascg, d=pcascg, s=vcbp.n, b=VDD)

        ### Nmos Mirror to top pmos Bias
        n2casc = ncasc(x=1)(g=ibias2, d=pbiasg, b=VSS)
        n2src = nbias(x=1)(g=ibias1, d=n2casc.s, s=VSS, b=VSS)

        ### Top Pmos Bias (with cascode)
        pdiode = pbias(x=1)(g=pbiasg, s=VDD, b=VDD)
        pdiode_casc = pcasc(x=1)(s=pdiode.d, g=pcascg, d=pbiasg, b=VDD)

        ## Compensation/ Load Cap
        ccc = h.Cap(c=params.cc * FEMTO)(p=out, n=VSS)

    return Fcasc


@h.generator
def FcascTb(params: TbParams) -> h.Module:
    """# Folded Cascode Op-Amp Testbench"""

    vicm = params.vicm or params.VDD / 2

    @h.module
    class OpAmpTb:
        VSS = h.Port()  # The testbench interface: sole port VSS

        # Drive VDD
        vdc = h.Vdc(dc=params.VDD)(n=VSS)
        inp = h.Diff()
        sig_out = h.Signal()
        sig_p = h.Vdc(dc=vicm, ac=+0.5)(p=inp.p, n=VSS)
        sig_n = h.Vdc(dc=vicm, ac=-0.5)(p=inp.n, n=VSS)

        # Primary difference: the two bias current inputs
        ibias1, ibias2 = 2 * h.Signal()
        xibias1 = h.Isrc(dc=params.ibias)(p=vdc.p, n=ibias1)
        xibias2 = h.Isrc(dc=params.ibias)(p=vdc.p, n=ibias2)

        # The Op-Amp DUT
        inst = params.dut(
            VDD=vdc.p, VSS=VSS, ibias1=ibias1, ibias2=ibias2, inp=inp, out=sig_out
        )

    return OpAmpTb


def endpoint(inp: FoldedCascodeInput) -> OpAmpOutput:
    """# Folded Cascode OpAmp RPC Implementation"""

    # Convert `inp` into the generator's parameters
    # params = as_hdl21_paramclass(inp)

    VDD = 1200 * MILLI
    ibias = 35 * MICRO

    # Create a testbench, simulate it, and return the metrics!
    opamp = Fcasc(**asdict(inp))
    tbparams = TbParams(
        dut=opamp, VDD=VDD, ibias=ibias, vicm=None  # Use the default common mode
    )
    tbmodule = FcascTb(tbparams)
    return simulate(tbmodule)
