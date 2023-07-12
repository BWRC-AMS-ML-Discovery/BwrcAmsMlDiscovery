# BWRC AMS ML Discovery

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
