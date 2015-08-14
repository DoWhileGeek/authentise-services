import pytest
import json
from authentise_services.session import Session
from authentise_services.config import Config
from authentise_services.model import Model
from urllib.parse import urljoin


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
    c = Config()
    c.host = "authentise.com"
    yield c

@pytest.yield_fixture
def session(httpretty, config):
    httpretty.register_uri(httpretty.POST,
                           "https://users.{}/sessions/".format(config.host),
                           forcing_headers={"Set-Cookie": "session=1234"},
                           status=200)

    yield Session("herp", "derp")

@pytest.yield_fixture
def model(httpretty, config, session):
    url = "http://derp.com/model/123/"

    payload = {"status": "processed",
               "name": "derp.stl"}

    httpretty.register_uri(httpretty.GET,
                           url,
                           body=json.dumps(payload),
                           status=200)

    yield Model(session, url=url)
