import json
from urllib.parse import urljoin

import pytest

from authentise_services import errors
from authentise_services.slice import Slice


def test_create_slice_resource_created(httpretty, config, session):
    dummy_url = "http://derp.com/"
    headers = {"Location": urljoin(dummy_url, "slice/123/")}

    payload = {"status": "processed",
               "config": urljoin(dummy_url, "config/123/"),
               "model": urljoin(dummy_url, "model/123/"),
               "content": urljoin(dummy_url, "content/123/"),
               "slice_time": 1234, }


    httpretty.register_uri(httpretty.POST,
                           "http://quickslice.{}/slice/".format(config.host),
                           adding_headers=headers,
                           status=200)

    httpretty.register_uri(httpretty.GET,
                           headers["Location"],
                           body=json.dumps(payload),
                           status=200)

    slice = Slice(session, model_uri=payload["model"], config_uri=payload["config"])

    assert slice.status == payload["status"]
    assert slice.location == headers["Location"]

def test_create_slice_resource_mix_and_match_created(httpretty, config, session, model):
    dummy_url = "http://derp.com/"
    headers = {"Location": urljoin(dummy_url, "slice/123/")}

    payload = {"status": "processed",
               "config": urljoin(dummy_url, "config/123/"),
               "model": urljoin(dummy_url, "model/123/"),
               "content": urljoin(dummy_url, "content/123/"),
               "slice_time": 1234, }


    httpretty.register_uri(httpretty.POST,
                           "http://quickslice.{}/slice/".format(config.host),
                           adding_headers=headers,
                           status=200)

    httpretty.register_uri(httpretty.GET,
                           headers["Location"],
                           body=json.dumps(payload),
                           status=200)

    slice = Slice(session, model=model, config_uri=payload["config"])

    assert slice.status == payload["status"]
    assert slice.location == headers["Location"]

@pytest.mark.xfail(raises=errors.ResourceError)
def test_create_slice_no_model_or_config(session):
    Slice(session)