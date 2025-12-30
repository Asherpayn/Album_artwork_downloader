"""Console output utilities with color formatting."""

# ANSI escape codes for color formatting
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


class ConsoleOutput:
    """Handles formatted console output with dependency injection for testability."""

    def __init__(self, print_fn=print):
        """
        Initialize with optional print function (for testing).

        Args:
            print_fn: Function to use for printing (default: built-in print)
        """
        self._print = print_fn

    def error(self, message: str) -> None:
        """
        Print error message in red.

        Args:
            message: Error message to display
        """
        self._print(f"{RED}{message}{RESET}")

    def success(self, message: str) -> None:
        """
        Print success message (default color).

        Args:
            message: Success message to display
        """
        self._print(message)

    def warning(self, message: str) -> None:
        """
        Print warning message in yellow.

        Args:
            message: Warning message to display
        """
        self._print(f"{YELLOW}{message}{RESET}")

    def info(self, message: str) -> None:
        """
        Print info message (default color).

        Args:
            message: Info message to display
        """
        self._print(message)

    def prompt(self, message: str, color: str = GREEN) -> str:
        """
        Print prompt and get user input.

        Args:
            message: Prompt message to display
            color: ANSI color code to use (default: GREEN)

        Returns:
            User input string
        """
        return input(f"{color}{message}{RESET}")
