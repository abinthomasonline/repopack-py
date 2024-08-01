import json
from typing import Dict, Any

DEFAULT_CONFIG = {
    "output": {
        "file_path": "repopack-output.txt",
        "style": "plain",
        "remove_comments": False,
        "remove_empty_lines": False,
    },
    "ignore": {
        "use_gitignore": True,
        "use_default_patterns": True,
        "custom_patterns": [],
    },
}

def load_config(config_path: str = None) -> Dict[str, Any]:
    if config_path:
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def merge_configs(file_config: Dict[str, Any], cli_config: Dict[str, Any]) -> Dict[str, Any]:
    merged = DEFAULT_CONFIG.copy()
    merged.update(file_config)
    merged.update(cli_config)
    return merged
