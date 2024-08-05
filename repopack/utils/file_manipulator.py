# file: utils/file_manipulator.py

import re


class FileManipulator:
    @staticmethod
    def remove_comments(content: str, file_extension: str) -> str:
        if file_extension in [".py", ".pyw"]:
            return FileManipulator.remove_python_comments(content)
        elif file_extension in [".js", ".ts", ".jsx", ".tsx"]:
            return FileManipulator.remove_js_comments(content)
        elif file_extension in [".html", ".htm"]:
            return FileManipulator.remove_html_comments(content)
        elif file_extension in [".css"]:
            return FileManipulator.remove_css_comments(content)
        else:
            print(f"Skipping comment removal for unknown file type: {file_extension}")
            return content  # No comment removal for unknown file types

    @staticmethod
    def remove_python_comments(content: str) -> str:
        # Remove single-line comments
        content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)
        # Remove multi-line comments
        content = re.sub(r'"""[\s\S]*?"""', "", content)
        content = re.sub(r"'''[\s\S]*?'''", "", content)
        return content

    @staticmethod
    def remove_js_comments(content: str) -> str:
        # Remove single-line comments
        content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
        # Remove multi-line comments
        content = re.sub(r"/\*[\s\S]*?\*/", "", content)
        return content

    @staticmethod
    def remove_html_comments(content: str) -> str:
        return re.sub(r"<!--[\s\S]*?-->", "", content)

    @staticmethod
    def remove_css_comments(content: str) -> str:
        return re.sub(r"/\*[\s\S]*?\*/", "", content)
