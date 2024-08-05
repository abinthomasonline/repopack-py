# file: exceptions.py

from typing import Optional


class RepopackError(Exception):
    """Base exception class for RepopackPy errors."""

    def __init__(self, message: Optional[str] = None) -> None:
        """
        Initialize the RepopackError.

        Args:
            message (Optional[str]): The error message. Defaults to None.
        """
        super().__init__(message)


class ConfigurationError(RepopackError):
    """Raised when there's an error in the configuration."""

    def __init__(self, message: str) -> None:
        """
        Initialize the ConfigurationError.

        Args:
            message (str): The specific configuration error message.
        """
        super().__init__(f"Configuration error: {message}")


class FileProcessingError(RepopackError):
    """Raised when there's an error processing a file."""

    def __init__(self, file_path: str, error_message: str) -> None:
        """
        Initialize the FileProcessingError.

        Args:
            file_path (str): The path of the file that caused the error.
            error_message (str): The specific error message.
        """
        super().__init__(f"Error processing file '{file_path}': {error_message}")


class OutputGenerationError(RepopackError):
    """Raised when there's an error generating the output."""

    def __init__(self, error_message: str) -> None:
        """
        Initialize the OutputGenerationError.

        Args:
            error_message (str): The specific error message related to output generation.
        """
        super().__init__(f"Error generating output: {error_message}")
