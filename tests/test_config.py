from authentise_services.config import Config

def test_config_no_config_file_happy_path():
    config = Config()
    assert config.host == "authentise.com"