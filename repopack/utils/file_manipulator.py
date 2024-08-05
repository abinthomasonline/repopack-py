# file: utils/file_manipulator.py

import re
from typing import Dict, List


class FileManipulator:
    """A utility class for manipulating file contents, primarily for removing comments."""

    # Mapping of file extensions to their respective comment removal methods
    EXTENSION_METHODS: Dict[str, str] = {
        ".py": "remove_python_comments",
        ".pyw": "remove_python_comments",
        ".js": "remove_js_comments",
        ".ts": "remove_js_comments",
        ".jsx": "remove_js_comments",
        ".tsx": "remove_js_comments",
        ".html": "remove_html_comments",
        ".htm": "remove_html_comments",
        ".css": "remove_css_comments",
    }

    @staticmethod
    def remove_comments(content: str, file_extension: str) -> str:
        """
        Remove comments from the given content based on the file extension.

        Args:
            content (str): The content to remove comments from.
            file_extension (str): The file extension to determine the comment style.

        Returns:
            str: The content with comments removed.
        """
        method_name = FileManipulator.EXTENSION_METHODS.get(file_extension)
        if method_name:
            method = getattr(FileManipulator, method_name)
            return method(content)
        else:
            print(f"Skipping comment removal for unknown file type: {file_extension}")
            return content  # No comment removal for unknown file types

    @staticmethod
    def remove_python_comments(content: str) -> str:
        """
        Remove Python-style comments from the given content.

        Args:
            content (str): The Python content to remove comments from.

        Returns:
            str: The content with Python comments removed.
        """
        # Remove single-line comments
        content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)
        # Remove multi-line comments (triple quotes)
        content = re.sub(r'"""[\s\S]*?"""', "", content)
        content = re.sub(r"'''[\s\S]*?'''", "", content)
        return content

    @staticmethod
    def remove_js_comments(content: str) -> str:
        """
        Remove JavaScript-style comments from the given content.

        Args:
            content (str): The JavaScript content to remove comments from.

        Returns:
            str: The content with JavaScript comments removed.
        """
        # Remove single-line comments
        content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
        # Remove multi-line comments
        content = re.sub(r"/\*[\s\S]*?\*/", "", content)
        return content

    @staticmethod
    def remove_html_comments(content: str) -> str:
        """
        Remove HTML-style comments from the given content.

        Args:
            content (str): The HTML content to remove comments from.

        Returns:
            str: The content with HTML comments removed.
        """
        return re.sub(r"<!--[\s\S]*?-->", "", content)

    @staticmethod
    def remove_css_comments(content: str) -> str:
        """
        Remove CSS-style comments from the given content.

        Args:
            content (str): The CSS content to remove comments from.

        Returns:
            str: The content with CSS comments removed.
        """
        return re.sub(r"/\*[\s\S]*?\*/", "", content)
