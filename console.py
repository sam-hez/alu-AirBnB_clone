#!/usr/bin/python3
"""Run the AirBnB clone command interpreter."""
import cmd


class HBNBCommand(cmd.Cmd):
    """Provide a basic command prompt for the AirBnB clone."""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit the command interpreter."""
        return True

    def do_EOF(self, arg):
        """Exit when the input ends or Ctrl-D is pressed."""
        print()
        return True

    def emptyline(self):
        """Ignore an empty line instead of repeating a command."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
