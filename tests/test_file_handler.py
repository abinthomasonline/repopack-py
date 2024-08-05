from unittest.mock import patch, mock_open
from typing import Dict, Any
from repopack.utils.file_handler import is_binary, sanitize_file


def test_is_binary() -> None:
    """
    Test if a binary file is correctly identified.
    """
    with patch("builtins.open", mock_open(read_data=b"\x00\x01\x02\x03")) as mock_file:
        mock_file.return_value.__enter__.return_value.read.return_value = b"\x00\x01\x02\x03"
        assert is_binary("fake_binary_file")


def test_is_not_binary() -> None:
    """
    Test if a text file is correctly identified as non-binary.
    """
    with patch("builtins.open", mock_open(read_data=b"Hello, World!")) as mock_file:
        mock_file.return_value.__enter__.return_value.read.return_value = b"Hello, World!"
        assert not is_binary("fake_text_file")


def test_sanitize_file() -> None:
    """
    Test if a file is correctly sanitized according to the given configuration.
    """
    config: Dict[str, Any] = {
        "output": {"remove_comments": False, "remove_empty_lines": True, "show_line_numbers": True}
    }
    content: str = "Line 1\n\nLine 3\n"
    expected: str = "1 | Line 1\n2 | Line 3"

    with patch("builtins.open", mock_open(read_data=content.encode())):
        result: str = sanitize_file("fake_file.txt", config)

    assert result == expected
