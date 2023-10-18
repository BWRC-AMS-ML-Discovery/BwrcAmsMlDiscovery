# BWRC AMS ML Discovery

Implementation of the `CktGym` project's ML-client & circuit-server architecture. 

Includes: 

- The [Discovery](./Discovery/) client and server libraries 
- A simple [Example](./Example/) use case
- The re-implementation of the [AutoCkt](./AutoCkt/) framework using [Discovery](./Discovery/) 

## [Discovery](./Discovery/) Libraries

Use these to create a new server instance pair. Read into this to understand how the server and client are setup, how they use shared utils to interact, and support simulations.

1. `cktgym_discovery_client`: focusing on authentication functions that sets up everything to be sent to server for requests using Firestore
2. `cktgym_discovery_server`: authenticates requests sent by clients and registers their rpcs to be used in simulations. The actual authentication function are under `auth`.
3. `cktgym_discovery_shared`: a shared folder for utils to be used by both client and server, and the most important part: the definition and implementation of the rpcs under the `rpc.py`.

## [Example](./Example) Use Case

Example is a use case of `discovery_client` and `discovery_server`, exposing a single simple endpoint. Read it first to understand how the (./Discovery/) servers as a trunk that hosts server functionalities and essential server - client interactions.

## [AutoCkt](./AutoCkt/) 

AutoCkt uses the server client interaction from (./Discovery/) to run the ML environment and provide it with necessary information to use proprietary software in (./Discovery/)

`autockt_shared` under `AutoCkt/Shared` contains the following:
1. data classes for rpcs and defined rpc classes that are used for registering in the `discovery_shared`, which in terms of example AutoCkt, would be:
```sh
auto_ckt_sim_hdl21 = Rpc(
    name="auto_ckt_sim_hdl21",
    input_type=OpAmpInput,
    return_type=OpAmpOutput,
    docstring="Simulation on the Server",
)
```
2. reward function used for ML environment with Ray.

`eval_engines` under `AutoCkt/Ckt` creates a call for client to send to `discovery_server`, in terms of autockt, it is called under different names according to circuit types. The `TwoStageOpAmp.py` is used for AutoCkt's ML training script under `scripts`. One example:
```sh
@auto_ckt_sim_hdl21.impl
def auto_ckt_sim_hdl21(inp: OpAmpInput) -> OpAmpOutput:
    """# Our RPC Handler"""
    return opamp_inner(inp)
```
where the `opamp_inner()` is from `TwoStageOpAmp.py` under `eval_engines`.
And the sample training script called `train_opamp.py`

`autockt` under `AutoCkt/Auto` handles the input using a ML script defined here. The complete implementation are divided into three major parts for AutoCkt, all with the name `autockt_gym_...`. They are manager classes used to update the parameters and the gym environment implementation for correctly invoking the simulation environment with Ray. 

### Autockt: autockt contains three packages, autockt_auto, autockt_ckt, and autockt_shared

Currently hosted on our server. Autockt is a service that uses Keertana's auto circuit RL setup to find the optimal OpAmp design. 

We defined OpenAI Gym environment in `autockt_auto`, for RL training. 

In `autockt_ckt`, we defined methods to calculate FOM for a given set of design params. We use these methods to calculate RL rewards.

In `autockt_shared`, we defined supporting data classes for RL, which includes data classes like "Range". 

## Installation

Currently recommends Python == 3.10

Due to dependency issues, create two separate python environments, one for `client` and one for `server`. 
For client py env, run:
```sh
sh scripts/install_client.sh
```
And for server py env, run:
```sh
sh scripts/install_server.sh
```

## Running a Local Dev Server

```sh
python AutoCkt/scripts/start_server.py
```

## Running AutoCkt Training

```sh
python AutoCkt/scripts/train_general.py
```

## Running Tensorboard

The training checkpoints will be saved in your home directory under `ray_results/`.
Tensorboard can be used to load reward and loss plots using the command:

```sh
tensorboard --logdir dir/of/checkpoints
```

## Running Tests

```sh
pytest
```

## Authentication Token

1. To register and obtain the auth token, go to [website](https://cktgym-1.web.app/).
2. Put the auth token in the `.env` file as `DISCOVERY_AUTH_TOKEN`.

