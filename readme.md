# BWRC AMS ML Discovery

## BWRC AMS ML Discovery is now separated into three major parts:
### Discovery: Discovery contains two public packages that are `bwrc_discovery_client` and `bwrc_discovery_shared`. 

`bwrc_discovery_shared` is a collection of data classes used to support server side functions. 

`bwrc_discovery_client` contains client call methods that are accepted by the server. 

`bwrc_discovery_shared` provides a data class called `rpcs` that defines rpc functions to be used by the server.

 In `bwrc_discovery_client`, function called `_setup_server_rpcs` correctly registers these rpc classes to the server and instantiate/register them. 

### Example: Example contains three public packages that are `example_client`, `example_server`, and `example_shared`. 

`example_shared` contains data classes for rpcs and defined rpc classes that are used for registering in the `discovery_shared`, which in terms of example AutoCkt, would be:
```sh
auto_ckt_sim_hdl21 = Rpc(
    name="auto_ckt_sim_hdl21",
    input_type=AutoCktInput,
    return_type=AutoCktOutput,
    docstring="Simulation on the Server",
)
```
where AutoCktInput and AutoCktOutput are also contained in here.

`example_server` 

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

1. To register and obtain the auth token, go to [website](https://bwrc-ams-ml-discovery-firebase-save.vercel.app/enter).
2. Put the auth token in the `.env` file as `DISCOVERY_AUTH_TOKEN`.
