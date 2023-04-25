# BWRC AMS ML Discovery

## Installation

Recommend using a virtual environment
GCP Debian python version == 3.9

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
