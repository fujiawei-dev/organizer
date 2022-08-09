import os

from organizer.config.settings import Settings, TMDb, yaml_config_settings_source
from tests.config.test_settings_data import create_temp_config_yml


def test_yaml_config_settings_source():
    config_yml_content = """
    log_level: DEBUG
    src: src
    dst: dst

    tmdb:
        api_key: api_key
    """
    config_file = create_temp_config_yml(content=config_yml_content)
    settings = Settings(config_file=config_file)
    source = yaml_config_settings_source(settings)

    assert isinstance(source, dict)
    assert source.get("log_level") == "DEBUG"
    assert source.get("src") == "src"
    assert source.get("dst") == "dst"
    assert source.get("tmdb").get("api_key") == "api_key"

    config_file.unlink(missing_ok=True)

    assert (
        yaml_config_settings_source(
            Settings(
                src="",
                dst="",
                config_file="missing_config.yml",
                tmdb=TMDb(api_key=""),
            )
        )
        == {}
    )


def test_settings():
    config_yml_content = """
    log_level: DEBUG
    src: src
    dst: dst
    """
    config_file = create_temp_config_yml(content=config_yml_content)
    api_key = os.getenv("TMDB__API_KEY")

    assert api_key

    os.environ["LOG_LEVEL"] = "INFO"
    os.environ["TMDB__API_KEY"] = "TMDB__API_KEY"
    settings = Settings(config_file=config_file, src="src_dir")

    assert settings.log_level == "DEBUG"
    assert settings.src == "src_dir"
    assert settings.dst == "dst"
    assert settings.tmdb.api_key == "TMDB__API_KEY"
    assert os.getenv("TMDB__API_KEY") == "TMDB__API_KEY"

    os.environ["TMDB__API_KEY"] = api_key
    config_file.unlink(missing_ok=True)
