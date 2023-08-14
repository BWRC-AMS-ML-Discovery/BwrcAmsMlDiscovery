from dotenv import dotenv_values
from example_server import example_server_start, Config

env = dotenv_values()

THE_SERVER_HOST = env.get("THE_SERVER_HOST", None)
if not THE_SERVER_HOST:
    raise ValueError("THE_SERVER_HOST not set in .env file")

THE_SERVER_PORT = env.get("THE_SERVER_PORT", None)
if not THE_SERVER_PORT:
    raise ValueError("THE_SERVER_PORT not set in .env file")

# Create the module-scope configuration
cfg = Config(port=THE_SERVER_PORT, host=THE_SERVER_HOST, enable_firebase_auth=False)
example_server_start(cfg)
