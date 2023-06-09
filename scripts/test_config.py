from discovery_client import (
    configure,
    options
)

def test_configure_client():
    configure(THE_SERVER_URL="a")
    assert "a" == options["THE_SERVER_URL"]
