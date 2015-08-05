import pytest

from authentise_services import errors
from authentise_services.session import Session


@pytest.mark.parametrize('status_code', [201,
                                         pytest.mark.xfail((403), raises=errors.ResourceError),
])
def test_create_user(config, httpretty, status_code):
    httpretty.register_uri(httpretty.POST,
                           "https://users.{}/users/".format(config.host),
                           status=status_code)

    Session.create_user("herp", "derp", "herp", "herp@derp.com")


@pytest.mark.parametrize('status_code', [201,
                                         pytest.mark.xfail((403), raises=errors.ResourceError),
])
def test_create_session(config, httpretty, status_code):
    httpretty.register_uri(httpretty.POST,
                           "https://users.{}/sessions/".format(config.host),
                           forcing_headers={"Set-Cookie": "session=1234"},
                           status=status_code)

    Session("herp", "derp")
