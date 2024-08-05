# file: exceptions.py


class RepopackError(Exception):
    """Base exception class for Repopack errors."""

    pass


class ConfigurationError(RepopackError):
    """Raised when there's an error in the configuration."""

    pass


class FileProcessingError(RepopackError):
    """Raised when there's an error processing a file."""

    pass


class OutputGenerationError(RepopackError):
    """Raised when there's an error generating the output."""

    pass
