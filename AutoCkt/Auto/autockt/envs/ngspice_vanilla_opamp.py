"""
A new ckt environment based on a new structure of MDP
"""

# Std-Lib Imports
import os, pickle, random
from dataclasses import fields

# from collections import OrderedDict

# PyPi Imports
import numpy as np
import gym
from gym import spaces

# Workspace Imports
from .create_design_and_simulate_lib import create_design_and_simulate
from shared import Range, CktInput, Params, Normalize, TargetSpecs, Spec
from eval_engines import PARAMS_RANGE, NORM_CONSTANT, TARGET_RANGE

# FIXME Avoid storing files?
SPECS_DIR = "/tmp/ckt_da_new/specs/"
PARAMS_RANGE = PARAMS_RANGE
NORM_CONSTANT = NORM_CONSTANT
TARGET_RANGE = TARGET_RANGE


class ParamManager:
    """
    A Processor for Managing Parameters handling
    input and output and other mechanism inside RL script
    """

    def __init__(self):
        self.spec = None
        self.params = None
        self.norm = None

    def load_spec(self, params: list, target: list, norm: list) -> CktInput:
        """
        params: parameters range, n# of ranges with step sizes, n * 3 for each [min, max, step]
        target: ideal spec range, n# of ranges without step sizes, n * 2 for each [min, max]
        norm: normalizing constants, 4# of constraints
        """
        params_values = {
            param[0]: Range(param[1][0], param[1][1], param[1][2]) for param in params
        }
        target_values = {
            target_[0]: Range(target_[1][0], target_[1][1]) for target_ in target
        }

        normalize_values = {norm_[0]: norm_[1] for norm_ in norm}

        ckt = CktInput(
            Params(params_values),
            Normalize(normalize_values),
            TargetSpecs(target_values),
        )

        self.params = Params(params_values)
        self.spec = TargetSpecs(target_values)
        self.norm = Normalize(normalize_values)
        return ckt

    def get_spec(self) -> Spec:
        """
        return the spec for initial setup
        """
        return self.spec

    def get_param(self) -> Params:
        """
        return the parameters passed in for initial setup
        """
        return self.params

    def get_norm(self) -> Spec:
        """
        return the normalizing constants passed in for initial setup
        """
        return self.norm


class TwoStageAmp(gym.Env):
    metadata = {
        "render.modes": ["human"],
    }

    PERF_LOW = -np.inf
    PERF_HIGH = np.inf

    # obtains yaml file
    # CIR_YAML = SPECS_DIR + "in/two_stage_opamp.yaml"

    def __init__(self, env_config):
        # Custom attributes (not from gym.Env)

        # control ideal specs
        self.multi_goal = env_config.get("multi_goal", False)
        self.generalize = env_config.get("generalize", False)

        # specs related
        self.specs_save = env_config.get("save_specs", False)  # Right now, never saved

        # validation related
        self.num_valid = env_config.get("num_valid", 50)  # Only used for validation
        self.valid = env_config.get("run_valid", False)  # Is running validation
        self.obj_idx = 0  # objective number (used for validation)

        # load specs and params
        self.pm = ParamManager()
        self._load_specs()
        self._save_specs()

        # initialize sim environment
        self.env_steps = 0
        self.action_meaning = [-1, 0, 2]
        self._set_gym_attributes()

        # initialize current param/spec observations

        # [0., 0., 0., 0.]
        self.cur_specs = np.zeros(len(self.specs_id), dtype=np.float32)

        # [0, 0, 0, 0, 0, 0, 0]
        self.cur_params_idx = np.zeros(len(self.params_id), dtype=np.int32)

    def reset(self):
        """
        Called when horizon is reached (or when env is reset, which never happens in our code)
        """
        self._set_ideal_specs()

        # initialize current parameters
        self.cur_params_idx = np.array([33, 33, 33, 33, 33, 14, 20])
        self.cur_specs = self.update(self.cur_params_idx)

        # reward
        reward = self.reward(self.cur_specs, self.specs_ideal)

        # applicable only when you have multiple goals, normalizes everything to some global_g
        self.specs_ideal_norm = self.lookup(self.specs_ideal, self.global_g)

        # observation is a combination of current specs distance from ideal, ideal spec, and current param vals
        cur_spec_norm = self.lookup(self.cur_specs, self.global_g)
        self.ob = np.concatenate(
            [cur_spec_norm, self.specs_ideal_norm, self.cur_params_idx]
        )
        return self.ob

    def step(self, action):
        """
        :param action: is vector with elements between 0 and 1 mapped to the index of the corresponding parameter
        :return:
        """

        self._take_action_to_update_params(action)

        # Get current specs and normalize
        self.cur_specs = self.update(self.cur_params_idx)
        reward = self.reward(self.cur_specs, self.specs_ideal)

        # incentivize reaching goal state
        done = False
        if reward >= 10:
            # ? In gym, done does not automatically call reset, but ray resets it when done?
            done = True
            print("-" * 10)
            print("params = ", self.cur_params_idx)
            print("specs:", self.cur_specs)
            print("ideal specs:", self.specs_ideal)
            print("re:", reward)
            print("-" * 10)

        # observation
        cur_spec_norm = self.lookup(self.cur_specs, self.global_g)
        self.ob = np.concatenate(
            [cur_spec_norm, self.specs_ideal_norm, self.cur_params_idx]
        )

        # states
        self.env_steps = self.env_steps + 1

        # print('cur ob:' + str(self.cur_specs))
        # print('ideal spec:' + str(self.specs_ideal))
        # print(reward)
        return self.ob, reward, done, {}

    def lookup(self, spec, goal_spec):
        """
        Normalizes (so-called) spec to goal_spec
        """
        goal_spec = [float(e) for e in goal_spec]
        norm_spec = (spec - goal_spec) / (goal_spec + spec)
        return norm_spec

    def reward(self, spec, goal_spec):
        """
        Reward: doesn't penalize for overshooting spec, is negative
        """
        rel_specs = self.lookup(spec, goal_spec)
        pos_val = []
        reward = 0.0
        for i, rel_spec in enumerate(rel_specs):
            if self.specs_id[i] == "ibias_max":
                rel_spec = rel_spec * -1.0  # /10.0
            if rel_spec < 0:
                reward += rel_spec
                pos_val.append(0)
            else:
                pos_val.append(1)

        return reward if reward < -0.02 else 10

    def update(self, params_idx):
        """

        :param action: an int between 0 ... n-1
        :return:
        """

        ## FIXME: Very important to understand this params stuff!

        # impose constraint tail1 = in
        # params_idx[0] = params_idx[3]

        # [34, 34, 34, 34, 34, 15, 2.1e-12]
        params = [
            self.params.ranges[param_id].get_value_at_index(params_idx[i])
            for i, param_id in enumerate(self.params_id)
        ]

        # OrderedDict([('mp1', 34), ('mn1', 34), ('mp3', 34), ('mn3', 34), ('mn4', 34), ('mn5', 15), ('cc', 2.1e-12)])
        param_val = dict(list(zip(self.params_id, params)))

        # run param vals and simulate
        cur_specs = dict(
            sorted(
                #
                # !!! Important replacement
                #
                create_design_and_simulate(param_val).items(),
                key=lambda k: k[0],
            )
        )
        cur_specs = np.array(list(cur_specs.values()))

        return cur_specs

    def _load_specs(self):
        # assign parameter range
        params = PARAMS_RANGE
        # assign normalizing constants
        norm = NORM_CONSTANT
        # assign target spec range
        target = TARGET_RANGE

        # input spec into manager
        self.pm.load_spec(params, target, norm)
        self.specs = self.pm.get_spec()
        self.params = self.pm.get_param()

        # To be filled in later
        self.specs_ideal = []

        # ['gain_min', 'ibias_max', 'phm_min', 'ugbw_min']
        self.specs_id = list(self.specs.ranges.keys())

        # ['mp1', 'mn1', 'mp3', 'mn3', 'mn4', 'mn5', 'cc']
        self.params_id = list(self.params.ranges.keys())

        # num_specs (originally 350)
        self.num_os = len(list(self.specs.ranges.values())[0])

        # Get the g* (overall design spec) you want to reach
        # Only when generalize=False and multi-goal=False

        self.global_g = []
        self.fixed_goal_idx = -1
        for spec in list(self.specs.ranges.values()):
            self.global_g.append(float(spec.get_value_at_index(self.fixed_goal_idx)))

        self.g_star = np.array(self.global_g)

        self.global_g = np.array(list(self.pm.get_norm().constants.values()))

    def _save_specs(self):
        if self.specs_save:
            with open(
                "specs_" + str(self.num_valid) + str(random.randint(1, 100000)), "wb"
            ) as f:
                pickle.dump(self.specs, f)

    def _set_gym_attributes(self):
        # Tuple(Discrete(3), Discrete(3), Discrete(3), Discrete(3), Discrete(3), Discrete(3), Discrete(3))
        self.action_space = spaces.Tuple(
            [spaces.Discrete(len(self.action_meaning))] * len(self.params_id)
        )

        # Each spec from PERF_LOW to PERF_HIGH, and each param from 1 to 1 (constant)
        # ! which is actually wrong! every slot can go out of bounds!
        self.observation_space = spaces.Box(
            low=np.array(
                [TwoStageAmp.PERF_LOW] * 2 * len(self.specs_id)
                + len(self.params_id) * [TwoStageAmp.PERF_LOW]
            ),
            high=np.array(
                [TwoStageAmp.PERF_HIGH] * 2 * len(self.specs_id)
                + len(self.params_id) * [TwoStageAmp.PERF_HIGH]
            ),
        )

    def _set_ideal_specs(self):
        # if multi-goal is selected, every time reset occurs, it will select a different design spec as objective
        if self.generalize == True:
            if self.valid == True:
                if self.obj_idx > self.num_os - 1:
                    self.obj_idx = 0
                idx = self.obj_idx
                self.obj_idx += 1
            else:
                idx = random.randint(0, self.num_os - 1)
            self.specs_ideal = []
            for spec in list(self.specs.ranges.values()):
                self.specs_ideal.append(spec.get_value_at_index(idx))
            self.specs_ideal = np.array(self.specs_ideal)
        else:
            if self.multi_goal == False:
                self.specs_ideal = self.g_star
            else:
                idx = random.randint(0, self.num_os - 1)
                self.specs_ideal = []
                for spec in list(self.specs.ranges.values()):
                    self.specs_ideal.append(spec[idx])
                self.specs_ideal = np.array(self.specs_ideal)

        # array([2.42000000e+02, 3.34670575e-03, 6.00000000e+01, 2.18719243e+07])
        # self.specs_ideal

        # print("num total:"+str(self.num_os))

    def _take_action_to_update_params(self, action):
        # Take action that RL agent returns to change current params
        # [2, 1, 2, 2, 1, 1, 2]
        action = list(np.reshape(np.array(action), (np.array(action).shape[0],)))

        # Move left or right
        self.cur_params_idx = self.cur_params_idx + np.array(
            [self.action_meaning[a] for a in action]
        )

        # Clip to make sure indexes do not go out of bounds
        self.cur_params_idx = np.clip(
            self.cur_params_idx,
            [0] * len(self.params_id),
            [len(getattr(self.params, field.name)) for field in fields(self.params)],
        )
