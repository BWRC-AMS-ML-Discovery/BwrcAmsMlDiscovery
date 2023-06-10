from discovery_client import (
    configure,
    options
)

from discovery_server import (
    configure,
    start_server
)

def test_configure_client():
    configure(THE_SERVER_URL="a")
    assert "a" == options["THE_SERVER_URL"]


start_server()