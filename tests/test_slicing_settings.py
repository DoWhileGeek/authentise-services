import json
import tempfile
from os.path import join

import pytest

from authentise_services import errors
from authentise_services.slicing_settings import SlicingSettings


@pytest.mark.parametrize('engine', ["slic3r",
                                    pytest.mark.xfail((None), raises=errors.ResourceError),
])
def test_create_slicing_settings_resource(httpretty, config, session, engine):
    headers = {"Location": "http://quickslice.{}/config/abc-123/".format(config.host), }
    httpretty.register_uri(httpretty.POST,
                           "http://quickslice.{}/config/raw/".format(config.host),
                           adding_headers=headers,
                           status=200)

    settings = SlicingSettings(session, "tests/objects/slic3r.ini", engine)
    settings.location == headers["Location"]


def test_load_pre_existing_config_resource(httpretty, config, session):
    uri = "http://quickslice.{}/config/abc-123/".format(config.host)

    payload = {"description": "cube.stl",
               "status": "processed"}

    httpretty.register_uri(httpretty.GET,
                           uri,
                           body=json.dumps(payload),
                           status=200)

    settings = SlicingSettings(session, url=uri)

    assert settings.description == payload["description"]
    assert settings.location == uri


def test_download_slicing_settings_resource(httpretty, config, session):
    headers = {"Location": "http://quickslice.{}/config/abc-123/".format(config.host), }
    httpretty.register_uri(httpretty.POST,
                           "http://quickslice.{}/config/raw/".format(config.host),
                           adding_headers=headers,
                           status=200)

    settings = SlicingSettings(session, "tests/objects/slic3r.ini", "slic3r")
    settings.location == headers["Location"]

    with open("tests/objects/slic3r.ini") as slicing_settings_file:
        content = slicing_settings_file.read()

    config_resp_payload = {"content": "http://herp.com/"}
    httpretty.register_uri(httpretty.GET,
                           headers["Location"],
                           body=json.dumps(config_resp_payload),
                           status=200)

    httpretty.register_uri(httpretty.GET,
                           config_resp_payload["content"],
                           body=content,
                           status=200)

    with tempfile.TemporaryDirectory() as temp_dir:
        path = join(temp_dir, "slic3r.ini")
        settings.download(path)

        with open(path) as downloaded_file:
            assert content == downloaded_file.read()


def test_unpopulated_slicing_settings(session):
    model = SlicingSettings(session)
    assert model.description == ""
    assert model.location == ""


def test_plain_string_session(session):
    model = SlicingSettings(str(session))
    assert model.description == ""
    assert model.location == ""
