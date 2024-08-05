from unittest.mock import patch
from repopack.utils.ignore_utils import (
    get_ignore_patterns,
    get_all_ignore_patterns,
    create_ignore_filter,
)


def test_get_ignore_patterns(tmp_path):
    ignore_file = tmp_path / ".gitignore"
    ignore_file.write_text("*.log\n#comment\nnode_modules/")

    patterns = get_ignore_patterns(".gitignore", str(tmp_path))
    assert patterns == ["*.log", "node_modules/"]


def test_get_all_ignore_patterns():
    config = {
        "ignore": {
            "use_default_patterns": True,
            "use_gitignore": True,
            "custom_patterns": ["*.custom"],
        }
    }
    with patch("repopack.utils.ignore_utils.get_ignore_patterns", return_value=["*.gitignore"]):
        patterns = get_all_ignore_patterns("/fake/path", config)

    assert "*.log" in patterns  # from DEFAULT_IGNORE_LIST
    assert "*.gitignore" in patterns  # from mocked .gitignore
    assert "*.custom" in patterns  # from custom patterns


def test_create_ignore_filter():
    patterns = ["*.log", "node_modules/"]
    ignore_filter = create_ignore_filter(patterns)

    assert not ignore_filter("test.log")
    assert not ignore_filter("node_modules/package.json")
    assert ignore_filter("src/main.py")
