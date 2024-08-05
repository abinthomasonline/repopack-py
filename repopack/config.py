import json
from typing import Dict, Any, Optional
from .exceptions import ConfigurationError


# Default configuration for RepopackPy
DEFAULT_CONFIG: Dict[str, Dict[str, Any]] = {
    "output": {
        "file_path": "repopackpy-output.txt",
        "style": "plain",
        "remove_comments": False,
        "remove_empty_lines": False,
        "top_files_length": 5,
        "show_line_numbers": False,
        "header_text": "",
    },
    "ignore": {
        "use_gitignore": True,
        "use_default_patterns": True,
        "custom_patterns": [],
    },
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    Args:
        config_path (Optional[str]): Path to the configuration file.

    Returns:
        Dict[str, Any]: Loaded configuration or an empty dictionary if no file is provided.

    Raises:
        ConfigurationError: If there's an error reading or parsing the configuration file.
    """
    if config_path:
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {str(e)}")
        except IOError as e:
            raise ConfigurationError(f"Error reading configuration file: {str(e)}")
    return {}


def merge_configs(file_config: Dict[str, Any], cli_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge configurations from different sources.

    Args:
        file_config (Dict[str, Any]): Configuration loaded from a file.
        cli_config (Dict[str, Any]): Configuration provided via command-line interface.

    Returns:
        Dict[str, Any]: Merged configuration.

    Raises:
        ConfigurationError: If there's an error during the merging process.
    """
    try:
        merged = DEFAULT_CONFIG.copy()
        merged = deep_merge(merged, file_config)
        merged = deep_merge(merged, cli_config)
        return merged
    except Exception as e:
        raise ConfigurationError(f"Error merging configurations: {str(e)}")


def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries.

    Args:
        dict1 (Dict[str, Any]): First dictionary to merge.
        dict2 (Dict[str, Any]): Second dictionary to merge.

    Returns:
        Dict[str, Any]: Merged dictionary.
    """
    for key, value in dict2.items():
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(value, dict):
                deep_merge(dict1[key], value)
            elif isinstance(dict1[key], list):
                if isinstance(value, list):
                    dict1[key].extend(value)
                else:
                    dict1[key].append(value)
            else:
                dict1[key] = value
        else:
            dict1[key] = value
    return dict1
