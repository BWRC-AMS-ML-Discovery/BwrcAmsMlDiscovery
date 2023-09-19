from example_shared import RingOscInput, RingOscOutput, ring_osc, ring_reward
from autockt import train

train(
    input_type=RingOscInput,
    output_type=RingOscOutput,
    simulation=ring_osc,
    reward=ring_reward,  # * ML people can change to override this
)
