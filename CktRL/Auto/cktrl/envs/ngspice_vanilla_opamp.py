"""
A new ckt environment based on a new structure of MDP
"""

# Std-Lib Imports
import os, pickle, random
# from collections import OrderedDict

# PyPi Imports
import numpy as np
import gym
from gym import spaces
import yaml
import yaml.constructor


# Workspace Imports
# from eval_engines.util.core import *
from eval_engines.ngspice.TwoStageClass import *


# FIXME Avoid storing files?
SPECS_DIR = "/tmp/ckt_da_new/specs/"


# way of ordering the way a yaml file is read
class YAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__(self, *args, **kwargs):
        print("args type:", type(args), ", value:", args)
        print("kwargs type:", type(kwargs), ", value:", kwargs)
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor("tag:yaml.org,2002:map", type(self).construct_yaml_map)
        self.add_constructor("tag:yaml.org,2002:omap", type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        print("node type:", type(node), ", value:", node)
        data = dict()
        yield data
        value = self.construct_mapping(node)
        print("value type:", type(value), ", value:", value)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        print("node type:", type(node), ", value:", node)
        print("deep type:", type(deep), ", value:", deep)
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "expected a mapping node, but found %s" % node.id,
                node.start_mark,
            )

        mapping = dict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
            print("key type:", type(key), ", value:", key)
            print("value type:", type(value), ", value:", value)

        print("mapping type:", type(mapping), ", value:", mapping)
        return mapping



class TwoStageAmp(gym.Env):
    metadata = {"render.modes": ["human"]}

    PERF_LOW = -np.inf
    PERF_HIGH = np.inf

    CIR_YAML = SPECS_DIR + "in/two_stage_opamp.yaml"

    def __init__(self, env_config):
        self.multi_goal = env_config.get("multi_goal", False)
        self.generalize = env_config.get("generalize", False)
        num_valid = env_config.get("num_valid", 50)
        self.specs_save = env_config.get("save_specs", False)
        self.valid = env_config.get("run_valid", False)

        self.env_steps = 0

        # load YAML data
        with open(TwoStageAmp.CIR_YAML, "r") as f:
            yaml_data = yaml.load(f, YAMLLoader)

        # design specs
        specs = yaml_data["target_specs"] if self.generalize == False else self.load_specs()
        self.specs = dict(sorted(specs.items(), key = lambda k: k[0]))

        self.specs_ideal = []
        self.specs_id = list(self.specs.keys())

        # param array
        params = yaml_data["params"]
        self.params = []
        self.params_id = list(params.keys())
        for value in params.values():
            param_vec = np.arange(value[0], value[1], value[2])
            self.params.append(param_vec)

        # initialize sim environment
        self.sim_env = TwoStageClass(yaml_path=TwoStageAmp.CIR_YAML, num_process=1)
        self.define_action_space()

        # initialize current param/spec observations
        self.cur_specs = np.zeros(len(self.specs_id), dtype=np.float32)
        self.cur_params_idx = np.zeros(len(self.params_id), dtype=np.int32)

        # Set the global goal
        self.global_g = np.array(yaml_data["normalize"])

    def load_specs(self):
        load_specs_path = SPECS_DIR + "out/ngspice_specs_gen_two_stage_opamp"
        with open(load_specs_path, "rb") as f:
            return pickle.load(f)

    def define_action_space(self):
        self.action_meaning = [-1, 0, 2]
        self.action_space = spaces.Tuple(
            [spaces.Discrete(len(self.action_meaning))] * len(self.params_id)
        )
        self.observation_space = spaces.Box(
            low=np.array([TwoStageAmp.PERF_LOW] * 2 * len(self.specs_id) + len(self.params_id) * [-np.inf]),
            high=np.array([TwoStageAmp.PERF_HIGH] * 2 * len(self.specs_id) + len(self.params_id) * [np.inf]),
        )


    def reset(self):
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
            for spec in list(self.specs.values()):
                self.specs_ideal.append(spec[idx])
            self.specs_ideal = np.array(self.specs_ideal)
        else:
            if self.multi_goal == False:
                self.specs_ideal = self.g_star
            else:
                idx = random.randint(0, self.num_os - 1)
                self.specs_ideal = []
                for spec in list(self.specs.values()):
                    self.specs_ideal.append(spec[idx])
                self.specs_ideal = np.array(self.specs_ideal)
        # print("num total:"+str(self.num_os))

        # applicable only when you have multiple goals, normalizes everything to some global_g
        self.specs_ideal_norm = self.lookup(self.specs_ideal, self.global_g)

        # initialize current parameters
        ## FIXME understand this 
        self.cur_params_idx = np.array([33, 33, 33, 33, 33, 14, 20]) 
        self.cur_specs = self.update(self.cur_params_idx)
        cur_spec_norm = self.lookup(self.cur_specs, self.global_g)
        reward = self.reward(self.cur_specs, self.specs_ideal)

        # observation is a combination of current specs distance from ideal, ideal spec, and current param vals
        self.ob = np.concatenate(
            [cur_spec_norm, self.specs_ideal_norm, self.cur_params_idx]
        )
        return self.ob


    def step(self, action):
        """
        :param action: is vector with elements between 0 and 1 mapped to the index of the corresponding parameter
        :return:
        """

        # Take action that RL agent returns to change current params
        action = list(np.reshape(np.array(action), (np.array(action).shape[0],)))
        self.cur_params_idx = self.cur_params_idx + np.array(
            [self.action_meaning[a] for a in action]
        )

        #self.cur_params_idx = self.cur_params_idx + np.array(self.action_arr[int(action)])
        self.cur_params_idx = np.clip(
            self.cur_params_idx,
            [0] * len(self.params_id),
            [(len(param_vec) - 1) for param_vec in self.params],
        )

        # Get current specs and normalize
        self.cur_specs = self.update(self.cur_params_idx)
        cur_spec_norm = self.lookup(self.cur_specs, self.global_g)
        reward = self.reward(self.cur_specs, self.specs_ideal)
        done = False

        # incentivize reaching goal state
        if reward >= 10:
            done = True
            print("-" * 10)
            print("params = ", self.cur_params_idx)
            print("specs:", self.cur_specs)
            print("ideal specs:", self.specs_ideal)
            print("re:", reward)
            print("-" * 10)

        self.ob = np.concatenate(
            [cur_spec_norm, self.specs_ideal_norm, self.cur_params_idx]
        )
        self.env_steps = self.env_steps + 1

        # print('cur ob:' + str(self.cur_specs))
        # print('ideal spec:' + str(self.specs_ideal))
        # print(reward)

        return self.ob, reward, done, {}


    def lookup(self, spec, goal_spec):
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
        params = [self.params[i][params_idx[i]] for i in range(len(self.params_id))]
        param_val = [dict(list(zip(self.params_id, params)))]

        # run param vals and simulate
        cur_specs = dict(
            sorted(
                #
                # FIXME: this call here gotta get replaced!
                #
                self.sim_env.create_design_and_simulate(param_val[0])[1].items(),
                key=lambda k: k[0],
            )
        )

        cur_specs = np.array(list(cur_specs.values()))

        return cur_specs

