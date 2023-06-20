#!/bin/bash
set -a # automatically export all variables
source .env
set +a # stop exporting all variables

uvicorn discovery_server:app --host $THE_SERVER_HOST --port $THE_SERVER_PORT --reload

