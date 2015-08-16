"""Model class module"""
import ntpath  # for windows support

import requests

from authentise_services import errors
from authentise_services.config import Config


class Slice(object):
    """Class representation of Slice resources."""

    def __init__(self, session, model=None, slicing_settings=None, model_uri=None, config_uri=None):
        try:
            config_uri = config_uri or slicing_settings.location
            model_uri = model_uri or model.location
        except AttributeError:
            raise errors.ResourceError

        self._state = None
        self.slice_time = None
        self.config = Config()
        try:  # catches session objects and session strings, probably horrible
            self.session = session.session
        except AttributeError:
            self.session = session
        
        self._create_slice_request(model_uri, config_uri)

    def __str__(self):
        return self.location

    def download(self, path):
        """downloads finished gcode to the destination"""
        service_get_resp = requests.get(self.location, cookies={"session": self.session})
        payload = service_get_resp.json()
        self._state = payload["status"]
        self.slice_time = payload["slice_time"]

        if self._state != "processed":
            raise errors.ResourceError("slice resource status is: {}".format(self._state))
        else:
            download_get_resp = requests.get(payload["content"])
            with open(path, "wb") as gcode_file:
                gcode_file.write(download_get_resp.content)

    def _create_slice_request(self, model_uri, config_uri):
        url = "http://quickslice.{}/slice/".format(self.config.host)
        resp = requests.post(url,
                             json={"model": model_uri, "config": config_uri},
                             cookies={"session": self.session})
        self.location = resp.headers["Location"]
        self._state = self._get_status()

    def _get_status(self):
        """utility method to get the status of a slicing job resource, but also used to initialize slice
            objects by location"""
        if self._state in ["processed", "error"]:
            return self._state
        
        get_resp = requests.get(self.location, cookies={"session": self.session})

        self._state = get_resp.json()["status"]
        self.slice_time = get_resp.json()["slice_time"]
        
        return self._state

    status = property(_get_status)
