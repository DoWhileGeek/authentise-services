"""Session class module"""
import requests

from authentise_services import errors
from authentise_services.config import Config


class Session(object):  # pylint: disable=too-few-public-methods
    """This class is for creating and holding onto user sessions for the model warehouse service"""

    def __init__(self, username=None, password=None):
        self.session = self.__create_session(username, password)

    def __str__(self):
        return self.session

    @staticmethod
    def __create_session(username=None, password=None):
        """grabs the configuration, and makes the call to Authentise to create the session"""
        config = Config()

        if not username or not password:
            username = config.username
            password = config.password

        payload = {
            "username": username,
            "password": password,
        }

        session_resp = requests.post("https://users.{}/sessions/".format(config.host), json=payload)
        if session_resp.status_code == 403:
            raise errors.ResourceError("bad user credentials")

        return session_resp.cookies["session"]

    @classmethod
    def create_user(cls, username, password, name, email):
        """utility class method to create a user"""
        config = Config()
        payload = {"username": username,
                   "email": email,
                   "name": name,
                   "password": password, }
        user_creation_resp = requests.post("https://users.{}/users/".format(config.host),
                                           json=payload)
        if user_creation_resp.status_code != 201:
            raise errors.ResourceError("couldnt create user")
