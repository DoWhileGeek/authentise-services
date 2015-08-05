import json
import tempfile
from os.path import join

from authentise_services.model import Model


def test_create_model_resource(httpretty, config, session):
    headers = {"Location": "https://models.{}/model/abc-123/".format(config.host),
               "X-Upload-Location": "https://abc-123.com/"}

    httpretty.register_uri(httpretty.POST,
                           "http://models.{}/model/".format(config.host),
                           adding_headers=headers,
                           status=200)

    httpretty.register_uri(httpretty.PUT,
                           headers["X-Upload-Location"],
                           status=200)

    model = Model(session, "tests/objects/cube.stl")

    assert model.name == "cube.stl"
    assert model.location == headers["Location"]


def test_load_pre_existing_model_resource(httpretty, config, session):
    uri = "http://models.{}/model/123/".format(config.host)

    payload = {"name": "cube.stl",
               "status": "processed"}

    httpretty.register_uri(httpretty.GET,
                           uri,
                           body=json.dumps(payload),
                           status=200)

    model = Model(session, url=uri)

    assert model.name == payload["name"]
    assert model.status == payload["status"]

def test_download_model_resource(httpretty, config, session):
    headers = {"Location": "https://models.{}/model/abc-123/".format(config.host),
               "X-Upload-Location": "https://abc-123.com/"}

    httpretty.register_uri(httpretty.POST,
                           "http://models.{}/model/".format(config.host),
                           adding_headers=headers,
                           status=200)

    httpretty.register_uri(httpretty.PUT,
                           headers["X-Upload-Location"],
                           status=200)

    model = Model(session, "tests/objects/cube.stl")

    assert model.name == "cube.stl"
    assert model.location == headers["Location"]

    model_payload = {"status": "processed",
                     "content": headers["X-Upload-Location"]}

    httpretty.register_uri(httpretty.GET,
                           headers["Location"],
                           body=json.dumps(model_payload),
                           status=200)

    with open("tests/objects/cube.stl") as model_file:
        content = model_file.read()

    httpretty.register_uri(httpretty.GET,
                       headers["X-Upload-Location"],
                       body=content,
                       status=200)

    with tempfile.TemporaryDirectory() as temp_dir:
        path = join(temp_dir, "model.stl")
        model.download(path)

        with open(path) as downloaded_file:
            assert content == downloaded_file.read()
