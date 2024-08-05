import pytest
from pathlib import Path
from typing import Dict, Any
from repopack.config import load_config, merge_configs, DEFAULT_CONFIG
from repopack.exceptions import ConfigurationError


def test_load_config(tmp_path: Path) -> None:
    """
    Test loading a valid configuration file.

    Args:
        tmp_path (Path): Pytest fixture providing a temporary directory path.
    """
    config_file: Path = tmp_path / "config.json"
    config_file.write_text('{"output": {"file_path": "custom_output.txt"}}')

    config: Dict[str, Any] = load_config(str(config_file))
    assert config["output"]["file_path"] == "custom_output.txt"


def test_load_config_invalid_json(tmp_path: Path) -> None:
    """
    Test loading an invalid JSON configuration file.

    Args:
        tmp_path (Path): Pytest fixture providing a temporary directory path.
    """
    config_file: Path = tmp_path / "invalid_config.json"
    config_file.write_text('{"output": {')

    with pytest.raises(ConfigurationError):
        load_config(str(config_file))


def test_merge_configs() -> None:
    """
    Test merging configurations from different sources.
    """
    file_config: Dict[str, Any] = {"output": {"file_path": "file_output.txt"}}
    cli_config: Dict[str, Any] = {"output": {"show_line_numbers": True}}
    merged: Dict[str, Any] = merge_configs(file_config, cli_config)

    assert merged["output"]["file_path"] == "file_output.txt"
    assert merged["output"]["show_line_numbers"] is True
    assert merged["output"]["style"] == DEFAULT_CONFIG["output"]["style"]
