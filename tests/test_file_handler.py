from unittest.mock import patch, mock_open
from repopack.utils.file_handler import is_binary, sanitize_file


def test_is_binary():
    with patch("builtins.open", mock_open(read_data=b"\x00\x01\x02\x03")):
        assert is_binary("fake_binary_file")


def test_is_not_binary():
    with patch("builtins.open", mock_open(read_data="Hello, World!")):
        assert not is_binary("fake_text_file")


def test_sanitize_file():
    config = {
        "output": {"remove_comments": False, "remove_empty_lines": True, "show_line_numbers": True}
    }
    content = "Line 1\n\nLine 3\n"
    expected = "1 | Line 1\n2 | Line 3"

    with patch("builtins.open", mock_open(read_data=content.encode())):
        result = sanitize_file("fake_file.txt", config)

    assert result == expected
