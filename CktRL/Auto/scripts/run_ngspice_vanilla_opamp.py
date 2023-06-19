if __name__ != "__main__":
    raise Exception("This is a SCRIPT and should be run as __main__!")

from cktrl.envs.ngspice_vanilla_opamp import TwoStageAmp
import IPython
import argparse
from cktrl.gen_specs import gen_data

SPECS_DIR = "/tmp/ckt_da_new/specs/"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_specs", type=str)
    args = parser.parse_args()
    CIR_YAML = SPECS_DIR + "in/two_stage_opamp.yaml"
    # Request user input for number of specifications
    num_specs = input("Please enter your number of specifications: ")

    # Use user input in the function
    gen_data(CIR_YAML, "two_stage_opamp", int(num_specs))

    env_config = {"generalize": True, "valid": True}
    env = TwoStageAmp(env_config)
    env.reset()
    env.step([2, 2, 2, 2, 2, 2, 2])
    IPython.embed()


main()
