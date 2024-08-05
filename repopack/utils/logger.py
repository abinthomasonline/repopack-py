import logging
from typing import Dict, Any
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages based on their level."""

    COLORS: Dict[str, str] = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.CYAN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with appropriate colors.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with color.
        """
        levelname: str = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        return super().format(record)


class Logger:
    """Custom logger class for RepoPackage."""

    def __init__(self) -> None:
        """Initialize the logger with a console handler and colored formatter."""
        self.logger: logging.Logger = logging.getLogger("repopack")
        self.logger.setLevel(logging.INFO)

        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
        self.logger.addHandler(console_handler)

    def set_verbose(self, verbose: bool) -> None:
        """
        Set the verbosity level of the logger.

        Args:
            verbose (bool): If True, set to DEBUG level; otherwise, set to INFO level.
        """
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)

    def trace(self, message: str) -> None:
        """
        Log a trace message if the logger level is set to DEBUG or lower.

        Args:
            message (str): The trace message to log.
        """
        if self.logger.level <= logging.DEBUG:
            self.logger.debug(f"{Fore.MAGENTA}TRACE: {message}{Style.RESET_ALL}")


# Create a global logger instance
logger: Logger = Logger()
