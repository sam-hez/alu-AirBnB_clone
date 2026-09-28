#!/usr/bin/python3
"""Test the basic command interpreter and piped input."""
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """Check help, exit commands, and blank input."""

    def setUp(self):
        """Create a console with captured output for each test."""
        self.output = io.StringIO()
        self.console = HBNBCommand(stdout=self.output)

    def test_prompt(self):
        """The console displays the required prompt."""
        self.assertEqual(self.console.prompt, "(hbnb) ")

    def test_quit(self):
        """The quit command tells the command loop to stop."""
        self.assertTrue(self.console.onecmd("quit"))

    def test_eof(self):
        """End of input stops the command loop and prints a newline."""
        with patch("sys.stdout", self.output):
            self.assertTrue(self.console.onecmd("EOF"))
        self.assertEqual(self.output.getvalue(), "\n")

    def test_help(self):
        """Help lists the supported commands."""
        self.console.onecmd("help")
        output = self.output.getvalue()
        for command in ("EOF", "help", "quit"):
            self.assertIn(command, output)

    def test_help_quit(self):
        """A command's help explains what it does."""
        self.console.onecmd("help quit")
        self.assertIn("Quit the command interpreter.",
                      self.output.getvalue())

    def test_empty_line(self):
        """Blank input does not repeat the previous command."""
        self.console.onecmd("help")
        self.output.seek(0)
        self.output.truncate(0)
        self.assertFalse(self.console.onecmd(""))
        self.assertEqual(self.output.getvalue(), "")

    def test_non_interactive(self):
        """Piped input supports both explicit quit and end of input."""
        script = Path(__file__).resolve().parents[1] / "console.py"
        for commands in ("help\nquit\n", "help\n"):
            with self.subTest(commands=commands):
                result = subprocess.run(
                    [sys.executable, str(script)], input=commands,
                    capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stderr, "")
                self.assertIn("(hbnb) ", result.stdout)
                self.assertIn("EOF  help  quit", result.stdout)


if __name__ == "__main__":
    unittest.main()
