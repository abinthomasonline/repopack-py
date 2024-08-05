from unittest.mock import patch
from pathlib import Path
from typing import List, Dict, Any, Callable
from repopack.utils.ignore_utils import (
    get_ignore_patterns,
    get_all_ignore_patterns,
    create_ignore_filter,
)


def test_get_ignore_patterns(tmp_path: Path) -> None:
    """
    Test the get_ignore_patterns function with a mock .gitignore file.

    Args:
        tmp_path (Path): Pytest fixture providing a temporary directory path.
    """
    ignore_file: Path = tmp_path / ".gitignore"
    ignore_file.write_text("*.log\n#comment\nnode_modules/")

    patterns: List[str] = get_ignore_patterns(".gitignore", str(tmp_path))
    assert patterns == ["*.log", "node_modules/"]


def test_get_all_ignore_patterns() -> None:
    """
    Test the get_all_ignore_patterns function with a mock configuration.
    """
    config: Dict[str, Any] = {
        "ignore": {
            "use_default_patterns": True,
            "use_gitignore": True,
            "custom_patterns": ["*.custom"],
        }
    }
    with patch("repopack.utils.ignore_utils.get_ignore_patterns", return_value=["*.gitignore"]):
        patterns: List[str] = get_all_ignore_patterns("/fake/path", config)

    assert "*.log" in patterns  # from DEFAULT_IGNORE_LIST
    assert "*.gitignore" in patterns  # from mocked .gitignore
    assert "*.custom" in patterns  # from custom patterns


def test_create_ignore_filter() -> None:
    """
    Test the create_ignore_filter function with sample patterns.
    """
    patterns: List[str] = ["*.log", "node_modules/"]
    ignore_filter: Callable[[str], bool] = create_ignore_filter(patterns)

    assert not ignore_filter("test.log")  # Should be ignored
    assert not ignore_filter("node_modules/package.json")  # Should be ignored
    assert ignore_filter("src/main.py")  # Should not be ignored
