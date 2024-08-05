import logging
from colorama import Fore, Style, init

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.CYAN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        return super().format(record)


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("repopack")
        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
        self.logger.addHandler(console_handler)

    def set_verbose(self, verbose: bool):
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def trace(self, message):
        if self.logger.level <= logging.DEBUG:
            self.logger.debug(f"{Fore.MAGENTA}TRACE: {message}{Style.RESET_ALL}")


logger = Logger()
