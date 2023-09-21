# BWRC AMS ML Discovery

Implementation of the `CktGym` project's ML-client & circuit-server architecture. 

Includes: 

- The [Discovery](./Discovery/) client and server libraries 
- A simple [Example](./Example/) use case
- The re-implementation of the [AutoCkt](./AutoCkt/) framework using [Discovery](./Discovery/) 

## [Discovery](./Discovery/) Libraries

Use these to create a new server instance pair. 

## [Example](./Example) Use Case

Example is a use case of `discovery_client` and `discovery_server`, exposing a single simple endpoint.

## [AutoCkt](./AutoCkt/) 

@wayne-wang start fixing from here

`example_shared` contains data classes for rpcs and defined rpc classes that are used for registering in the `discovery_shared`, which in terms of example AutoCkt, would be:
```sh
auto_ckt_sim_hdl21 = Rpc(
    name="auto_ckt_sim_hdl21",
    input_type=OpAmpInput,
    return_type=OpAmpOutput,
    docstring="Simulation on the Server",
)
```
where OpAmpInput and OpAmpOutput are also contained in here.

`example_client` creates a call for client to send to `example_server`, in terms of autockt, it is called `test_autockt_sim`. 

`example_server` handles the input sent from the client side, using a server function defined here. In terms of autockt, it would be:
```sh
@auto_ckt_sim_hdl21.impl
def auto_ckt_sim_hdl21(inp: OpAmpInput) -> OpAmpOutput:
    """
    AutoCkt Simulation
    """
```
which correctly uses the rpcs registered in the previous step in `bwrc_discovery`

### Autockt: autockt contains three packages, autockt_auto, autockt_ckt, and autockt_shared

Currently hosted on our server. Autockt is a service that uses Keertana's auto circuit RL setup to find the optimal OpAmp design. 

We defined OpenAI Gym environment in `autockt_auto`, for RL training. 

In `autockt_ckt`, we defined methods to calculate FOM for a given set of design params. We use these methods to calculate RL rewards.

In `autockt_shared`, we defined supporting data classes for RL, which includes data classes like "Range". 

## Installation

Currently recommends Python == 3.10

```sh
sh scripts/install.sh
```

## Running a Local Dev Server

```sh
python scripts/server_start.py
```

## Running Client Examples

```sh
python scripts/client_do_example_stuff.py
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
