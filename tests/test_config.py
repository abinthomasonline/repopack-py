import pytest
from repopack.config import load_config, merge_configs, DEFAULT_CONFIG
from repopack.exceptions import ConfigurationError


def test_load_config(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"output": {"file_path": "custom_output.txt"}}')

    config = load_config(str(config_file))
    assert config["output"]["file_path"] == "custom_output.txt"


def test_load_config_invalid_json(tmp_path):
    config_file = tmp_path / "invalid_config.json"
    config_file.write_text('{"output": {')

    with pytest.raises(ConfigurationError):
        load_config(str(config_file))


def test_merge_configs():
    file_config = {"output": {"file_path": "file_output.txt"}}
    cli_config = {"output": {"show_line_numbers": True}}
    merged = merge_configs(file_config, cli_config)

    assert merged["output"]["file_path"] == "file_output.txt"
    assert merged["output"]["show_line_numbers"] == True
    assert merged["output"]["style"] == DEFAULT_CONFIG["output"]["style"]
