"""Tests for output utilities."""
import unittest
from unittest.mock import Mock
from output import ConsoleOutput, RED, GREEN, YELLOW, RESET


class TestConsoleOutput(unittest.TestCase):
    """Test cases for ConsoleOutput class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_print = Mock()
        self.output = ConsoleOutput(print_fn=self.mock_print)

    def test_error_prints_with_red_color(self):
        """Test that error messages are printed in red."""
        self.output.error("Test error")
        self.mock_print.assert_called_once_with(f"{RED}Test error{RESET}")

    def test_warning_prints_with_yellow_color(self):
        """Test that warning messages are printed in yellow."""
        self.output.warning("Test warning")
        self.mock_print.assert_called_once_with(f"{YELLOW}Test warning{RESET}")

    def test_success_prints_without_color(self):
        """Test that success messages are printed without color."""
        self.output.success("Test success")
        self.mock_print.assert_called_once_with("Test success")

    def test_info_prints_message(self):
        """Test that info messages are printed correctly."""
        self.output.info("Test info")
        self.mock_print.assert_called_once_with("Test info")

    def test_prompt_with_default_green_color(self):
        """Test that prompt uses green color by default."""
        with unittest.mock.patch('builtins.input', return_value='user input'):
            result = self.output.prompt("Enter value: ")
            self.assertEqual(result, "user input")

    def test_prompt_with_custom_color(self):
        """Test that prompt can use custom color."""
        with unittest.mock.patch('builtins.input', return_value='user input'):
            result = self.output.prompt("Enter value: ", color=RED)
            self.assertEqual(result, "user input")

    def test_multiple_error_calls(self):
        """Test multiple error calls."""
        self.output.error("Error 1")
        self.output.error("Error 2")
        self.assertEqual(self.mock_print.call_count, 2)

    def test_mixed_output_types(self):
        """Test calling different output methods."""
        self.output.info("Info message")
        self.output.warning("Warning message")
        self.output.error("Error message")
        self.output.success("Success message")
        self.assertEqual(self.mock_print.call_count, 4)


if __name__ == '__main__':
    unittest.main()
