from dataclasses import dataclass


@dataclass
class OpAmpOutput:
    """# Op-Amp Output
    Server output type reused by several op-amp flavors"""

    gain: float
    ugbw: float
    phm: float
    ibias: float
