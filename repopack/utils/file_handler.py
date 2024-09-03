import os
import chardet
from typing import List, Dict, Any, Optional
from ..exceptions import FileProcessingError
from .file_manipulator import FileManipulator
from .logger import logger


def is_binary(file_path: str) -> bool:
    """
    Check if a file is binary.

    Args:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file is binary, False otherwise.
    """
    try:
        with open(file_path, "rb") as file:
            chunk = file.read(1024)
            return b"\0" in chunk  # Check for null bytes
    except IOError:
        return False


def sanitize_files(
    file_paths: List[str], root_dir: str, config: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    Sanitize files based on the given configuration.

    Args:
        file_paths (List[str]): List of file paths to sanitize.
        root_dir (str): The root directory of the project.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing sanitized file paths and contents.

    Raises:
        FileProcessingError: If there's an error processing a file.
    """
    sanitized_files = []
    for file_path in file_paths:
        full_path = os.path.join(root_dir, file_path)
        logger.trace(f"Sanitizing file: {file_path}")
        try:
            if not is_binary(full_path):
                content = sanitize_file(full_path, config)
                if content:
                    sanitized_files.append({"path": file_path, "content": content})
                    logger.trace(f"File sanitized: {file_path}")
                else:
                    logger.trace(f"File skipped (empty content): {file_path}")
        except Exception as e:
            raise FileProcessingError(file_path=file_path, error_message=str(e))
    return sanitized_files


def sanitize_file(file_path: str, config: Dict[str, Any]) -> Optional[str]:
    """
    Sanitize a single file.

    Args:
        file_path (str): The path to the file to sanitize.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        Optional[str]: The sanitized content of the file, or None if the file is empty.

    Raises:
        FileProcessingError: If there's an error sanitizing the file.
    """
    try:
        with open(file_path, "rb") as f:
            raw_content = f.read()

        # Detect file encoding
        encoding = chardet.detect(raw_content)["encoding"] or "utf-8"
        try:
            content = raw_content.decode(encoding)
            logger.trace(f"File encoding detected: {encoding}")
        except UnicodeDecodeError:
            logger.warning(f"Failed to decode with detected encoding {encoding}, trying UTF-8")
            content = raw_content.decode("utf-8")
            logger.trace("File decoded with UTF-8")

        # Remove comments (not implemented yet)
        if config["output"]["remove_comments"]:
            raise NotImplementedError("Comment removal is not implemented yet.")
            # file_extension = os.path.splitext(file_path)[1]
            # content = FileManipulator.remove_comments(content, file_extension)
            # logger.trace(f"Comments removed from file: {file_path}")

        # Remove empty lines if configured
        if config["output"]["remove_empty_lines"]:
            content = remove_empty_lines(content)
            logger.trace(f"Empty lines removed from file: {file_path}")

        content = content.strip()

        # Add line numbers if configured
        if config["output"]["show_line_numbers"]:
            content = add_line_numbers(content)
            logger.trace(f"Line numbers added to file: {file_path}")

        return content
    except Exception as e:
        raise FileProcessingError(file_path=file_path, error_message=str(e))


def remove_empty_lines(content: str) -> str:
    """
    Remove empty lines from the content.

    Args:
        content (str): The content to process.

    Returns:
        str: The content with empty lines removed.
    """
    return "\n".join(line for line in content.splitlines() if line.strip())


def add_line_numbers(content: str) -> str:
    """
    Add line numbers to the content.

    Args:
        content (str): The content to process.

    Returns:
        str: The content with line numbers added.
    """
    lines = content.split("\n")
    max_line_num = len(lines)
    line_num_width = len(str(max_line_num))
    return "\n".join(f"{str(i+1).rjust(line_num_width)} | {line}" for i, line in enumerate(lines))
