"""Config class module"""
import configparser  # pylint: disable=import-error
import os


class Config(object):
    """This class is for the modules that need authentise session and host info"""

    def __init__(self):
        self.path = self.find_config_file(["/srv/authentise_services/config.ini",
                                           os.path.expanduser("~/.authentise_services/config.ini"),
                                          ])

        config = self.parse_config(self.path)

        self.host = config.get("host", None)
        self.username = config.get("username", None)
        self.password = config.get("password", None)

    def __dir__(self):
        return {"host": self.host, "username": self.username, "password": self.password}

    @staticmethod
    def parse_config(path):
        """parse either the config file we found, or use some canned defaults"""
        config = configparser.ConfigParser()

        if path:  # if user has config with user creds in it, this will grab it
            config.read(path)

        config["default"] = {"host": "authentise.com", }

        return {k: v for k, v in config["default"].items()}

    @staticmethod
    def find_config_file(possible_paths):
        """given a list of different paths for different systems, return the first one we find"""
        for path in possible_paths:
            if os.path.isfile(path):
                return path
