from halo import Halo
from typing import Any


class Spinner:
    """A wrapper class for the Halo spinner to provide a simple interface for displaying progress."""

    def __init__(self, message: str) -> None:
        """
        Initialize the Spinner with a message.

        Args:
            message (str): The initial message to display with the spinner.
        """
        self.spinner: Halo = Halo(text=message, spinner="dots")

    def start(self) -> None:
        """Start the spinner animation."""
        self.spinner.start()

    def stop(self) -> None:
        """Stop the spinner animation."""
        self.spinner.stop()

    def succeed(self, message: str) -> None:
        """
        Display a success message and stop the spinner.

        Args:
            message (str): The success message to display.
        """
        self.spinner.succeed(message)

    def fail(self, message: str) -> None:
        """
        Display a failure message and stop the spinner.

        Args:
            message (str): The failure message to display.
        """
        self.spinner.fail(message)
