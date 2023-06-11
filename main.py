from fastapi import FastAPI
from Discovery.Server.discovery_server import app as discovery_app
from Example.Server.example_server import app as example_app

app = FastAPI()

app.mount("/Discovery", discovery_app)
app.mount("/Example", example_app)