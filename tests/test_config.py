from authentise_services.config import Config
import tempfile


def test_magic_dir_method():
    config = Config()
    assert dir(config) == ['host', 'password', 'username']


def test_load_config_file():
    config = Config(path="tests/objects/config.ini")

    assert config.username == "herp"
    assert config.password == "derp"
