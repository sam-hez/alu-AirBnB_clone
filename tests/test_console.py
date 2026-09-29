#!/usr/bin/python3
"""Test the basic command interpreter and piped input."""
import io
import ast
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User


class TestConsole(unittest.TestCase):
    """Check help, exit commands, and blank input."""

    def setUp(self):
        """Create a console with captured output for each test."""
        self.output = io.StringIO()
        self.console = HBNBCommand(stdout=self.output)
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "file.json"
        for name, value in (("_FileStorage__objects", {}),
                            ("_FileStorage__file_path", str(self.path))):
            patcher = patch.object(FileStorage, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_command(self, command):
        """Run a command and capture its printed response."""
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            self.console.onecmd(command)
        return output.getvalue()

    def test_argument_errors(self):
        """Commands report missing and invalid arguments in order."""
        for command in ("create", "show", "destroy", "update"):
            with self.subTest(command=command):
                self.assertEqual(self.run_command(command),
                                 "** class name missing **\n")
                self.assertEqual(self.run_command(command + " MyModel"),
                                 "** class doesn't exist **\n")
        for command in ("show", "destroy", "update"):
            with self.subTest(command=command):
                self.assertEqual(self.run_command(command + " BaseModel"),
                                 "** instance id missing **\n")
                self.assertEqual(
                    self.run_command(command + " BaseModel missing"),
                    "** no instance found **\n")
        self.assertEqual(self.run_command("all MyModel"),
                         "** class doesn't exist **\n")
        obj = BaseModel()
        command = "update BaseModel " + obj.id
        self.assertEqual(self.run_command(command),
                         "** attribute name missing **\n")
        self.assertEqual(self.run_command(command + " name"),
                         "** value missing **\n")
        self.assertFalse(self.path.exists())

    def test_create_show_destroy(self):
        """Creation and deletion persist, and show displays the object."""
        obj_id = self.run_command("create BaseModel").strip()
        key = "BaseModel." + obj_id
        obj = storage.all()[key]
        self.assertEqual(json.loads(self.path.read_text())[key],
                         obj.to_dict())
        self.assertEqual(self.run_command("show BaseModel " + obj_id),
                         str(obj) + "\n")
        self.assertEqual(self.run_command("destroy BaseModel " + obj_id),
                         "")
        self.assertNotIn(key, storage.all())
        self.assertEqual(json.loads(self.path.read_text()), {})
        self.assertEqual(self.run_command("show BaseModel " + obj_id),
                         "** no instance found **\n")

    def test_all_objects(self):
        """All returns a list of strings and supports class filtering."""
        self.assertEqual(self.run_command("all"), "[]\n")
        base = BaseModel()
        user = User()
        self.assertCountEqual(ast.literal_eval(self.run_command("all")),
                              [str(base), str(user)])
        self.assertEqual(ast.literal_eval(self.run_command("all BaseModel")),
                         [str(base)])

    def test_update_values(self):
        """Updates preserve types, quoted spaces, and saved values."""
        obj = BaseModel()
        obj.number = 1
        obj.price = 1.5
        prefix = "update BaseModel " + obj.id
        cases = (("name", '"Betty Smith"', "Betty Smith"),
                 ("number", "89", 89), ("price", "2.75", 2.75),
                 ("name", '""', ""))
        for name, value, expected in cases:
            with self.subTest(attribute=name, value=value):
                command = "{} {} {}".format(prefix, name, value)
                self.assertEqual(self.run_command(command), "")
                self.assertEqual(getattr(obj, name), expected)
                self.assertIs(type(getattr(obj, name)), type(expected))
                saved = json.loads(self.path.read_text())
                self.assertEqual(saved["BaseModel." + obj.id], obj.to_dict())
        self.run_command(prefix + ' name "First" number 100')
        self.assertEqual(obj.name, "First")
        self.assertEqual(obj.number, 89)

    def test_protected_attributes(self):
        """Updates do not replace IDs or timestamps."""
        obj = BaseModel()
        original = obj.to_dict()
        for name in ("id", "created_at", "updated_at"):
            self.run_command("update BaseModel {} {} changed".format(
                obj.id, name))
        self.assertEqual(obj.to_dict(), original)

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
                for command in ("EOF", "help", "quit", "create", "show",
                                "destroy", "all", "update"):
                    self.assertIn(command, result.stdout)


if __name__ == "__main__":
    unittest.main()
