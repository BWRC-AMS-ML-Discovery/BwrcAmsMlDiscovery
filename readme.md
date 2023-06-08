# BWRC AMS ML Discovery

## Installation New

Currently requires Python <= 3.10

```
sh scripts/install.sh
```

## Installation

```
pip install -e ".[dev]"
```

## Running a Local Dev Server

```
bash scripts/serve.sh
```

## Running Client Examples

```
python scripts/client_examples.py
```

## Authentication Token

1. To register and obtain the auth token, go to [website](https://bwrc-ams-ml-discovery-firebase-save.vercel.app/enter).
2. Put the auth token in the `.env` file as `DISCOVERY_AUTH_TOKEN`.
