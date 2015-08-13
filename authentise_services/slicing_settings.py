"""slicing_settings class module"""
import ntpath  # for windows support

import requests

from authentise_services import errors
from authentise_services.config import Config


class SlicingSettings(object):
    """Class representation of config resources."""
    def __init__(self, session, path=None, engine=None, description=None, url=None):
        self.config = Config()

        try:  # catches session objects and session strings, probably horrible
            self.session = session.session
        except AttributeError:
            self.session = session

        if path:
            if not engine:
                raise errors.ResourceError("resource creation requires path and engine supplied")
            self.upload(path, engine, description)
        elif url:
            self.location = url
            self._get_description()
        else:
            self.description = ""
            self.location = ""

    def upload(self, path, engine, description=None):
        """Create a new config resource in the slicing service and upload the path contents to it"""

        if description is None:
            head, tail = ntpath.split(path)
            description = tail or ntpath.basename(head)

        url = "http://quickslice.{}/config/raw/".format(self.config.host)

        with open(path) as config_file:
            content = config_file.read()

        payload = {"engine": engine,
                   "description": description,
                   "content": content}

        post_resp = requests.post(url, json=payload, cookies={"session": self.session})
        if not post_resp.ok:
            raise errors.ResourceError("upload to slicing service failed")

        self.description = description

        self.location = post_resp.headers["Location"]

    def download(self, path):
        """downloads a config resource to the path"""

        service_get_resp = requests.get(self.location, cookies={"session": self.session})
        payload = service_get_resp.json()

        download_get_resp = requests.get(payload["content"])
        with open(path, "wb") as config_file:
            config_file.write(download_get_resp.content)

    def _get_description(self):
        resp = requests.get(self.location, cookies={"session": self.session})

        self.description = resp.json()["description"]
