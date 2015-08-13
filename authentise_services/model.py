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
        self._state = None
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
            self.name = None
            self.location = None

    def __str__(self):
        return self.location

    def upload(self,  # pylint: disable=too-many-arguments
               path,
               name=None,
               resize=False,
               rotation=False,
               callback_url=None,
               callback_method=None,
               auto_align=False, ):
        """Create a new model resource in the warehouse and uploads the path contents to it"""
        if name is None:
            head, tail = ntpath.split(path)
            name = tail or ntpath.basename(head)

        url = "http://models.{}/model/".format(self.config.host)

        payload = {"name": name,
                   "allowed_transformations": {"resize": resize,
                                               "rotation": rotation, },
                   "auto-align": auto_align}
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
        self._state = self._get_status()

    def download(self, path):
        """downloads a model resource to the path"""
        service_get_resp = requests.get(self.location, cookies={"session": self.session})
        payload = service_get_resp.json()
        self._state = payload["status"]

        if self._state != "processed":
            raise errors.ResourceError("slice resource status is: {}".format(self._state))
        else:
            download_get_resp = requests.get(payload["content"])
            with open(path, "wb") as model_file:
                model_file.write(download_get_resp.content)

    def _get_status(self):
        """utility method to get the status of a model resource, but also used to initialize model
            objects by location"""

        if self._state in ["processed", "error"]:
            return self._state

        get_resp = requests.get(self.location, cookies={"session": self.session})
        self.name = get_resp.json()["name"]
        self._state = get_resp.json()["status"]
        return self._state

    status = property(_get_status)
