import json
from typing import Dict, Any
from .exceptions import ConfigurationError


DEFAULT_CONFIG = {
    "output": {
        "file_path": "repopack-output.txt",
        "style": "plain",
        "remove_comments": False,
        "remove_empty_lines": False,
        "top_files_length": 5,
        "show_line_numbers": False,
    },
    "ignore": {
        "use_gitignore": True,
        "use_default_patterns": True,
        "custom_patterns": [],
    },
}


def load_config(config_path: str = None) -> Dict[str, Any]:
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
    try:
        merged = DEFAULT_CONFIG.copy()
        merged = deep_merge(merged, file_config)
        merged = deep_merge(merged, cli_config)
        return merged
    except Exception as e:
        raise ConfigurationError(f"Error merging configurations: {str(e)}")


def deep_merge(dict1, dict2):
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
