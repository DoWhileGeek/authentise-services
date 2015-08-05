"""Model class module"""
import ntpath  # for windows support

import requests

from authentise_services import errors
from authentise_services.config import Config


class Model(object):
    """Class representation of Model resources."""

    def __init__(self, session, path=None, url=None, name=None, callback_url=None,
                 callback_method=None):
        self.config = Config()
        try:  # catches session objects and session strings, probably horrible
            self.session = session.session
        except AttributeError:
            self.session = session

        if path:
            self.upload(path, name=name, callback_url=callback_url, callback_method=callback_method)
        elif url:
            self.location = url
            self._get_status()
        else:
            self.name = ""
            self.location = ""

    def __str__(self):
        return self.location

    def upload(self,  # pylint: disable=too-many-arguments
               path,
               name=None,
               resize=False,
               rotation=False,
               callback_url=None,
               callback_method=None, ):
        """Create a new model resource in the warehouse and uploads the path contents to it"""
        if name is None:
            head, tail = ntpath.split(path)
            name = tail or ntpath.basename(head)

        url = "http://models.{}/model/".format(self.config.host)

        payload = {"name": name,
                   "allowed_transformations": {"resize": resize,
                                               "rotation": rotation, }, }
        if callback_url and callback_method:
            payload["callback"] = {"url": callback_url, "method": callback_method}

        post_resp = requests.post(url, json=payload, cookies={"session": self.session})
        if not post_resp.ok:
            raise errors.ResourceError("payload to model service invalid")

        self.name = name

        with open(path, "rb") as model_file:
            put_resp = requests.put(post_resp.headers["x-upload-location"],
                                    data=model_file.read(),
                                    headers={"Content-Type": "application/octet-stream"})
            if not put_resp.ok:
                raise errors.ResourceError("model upload failed")

        self.location = post_resp.headers["Location"]

    def download(self, destination):
        """downloads a model resource to the destination"""
        service_get_resp = requests.get(self.location, cookies={"session": self.session})
        payload = service_get_resp.json()

        if payload["status"] == "error":
            raise errors.ResourceError("model resource is unusable")
        elif payload["status"] in ["not-uploaded", "processing"]:
            raise errors.ResourceError("model resource is {}".format(payload["status"]))
        else:
            download_get_resp = requests.get(payload["content"])
            with open(destination, "wb") as model_file:
                model_file.write(download_get_resp.content)

    def _get_status(self):
        """utility method to get the status of a model resource, but also used to initialize model
            objects by location"""
        get_resp = requests.get(self.location, cookies={"session": self.session})
        self.name = get_resp.json()["name"]
        return get_resp.json()["status"]

    status = property(_get_status)
