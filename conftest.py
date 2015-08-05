import pytest
import json

import httpretty as HTTPretty

@pytest.yield_fixture
def httpretty():
    import socket
    old_socket_type = socket.SocketType
    HTTPretty.enable()
    yield HTTPretty
    HTTPretty.disable()
    socket.SocketType = old_socket_type
    HTTPretty.reset()

@pytest.yield_fixture
def config():
    from authentise_services.config import Config

    yield Config()

@pytest.yield_fixture
def session(httpretty, config):
    from authentise_services.session import Session

    httpretty.register_uri(httpretty.POST,
                           "https://users.{}/sessions/".format(config.host),
                           forcing_headers={"Set-Cookie": "session=1234"},
                           status=200)

    yield Session("herp", "derp")
