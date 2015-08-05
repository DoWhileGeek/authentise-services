from authentise_services.config import Config
import tempfile

def test_config_no_config_file_happy_path():
    config = Config()
    assert config.host == "authentise.com"


def test_magic_dir_method():
    config = Config()
    assert config.host == "authentise.com"
    assert dir(config) == ['host', 'password', 'username']


def test_load_config_file():
    config = Config(path="tests/objects/config.ini")

    assert config.username == "herp"
    assert config.password == "derp"
