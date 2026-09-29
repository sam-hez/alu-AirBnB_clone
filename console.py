#!/usr/bin/python3
"""Run the AirBnB clone command interpreter."""
import cmd
import shlex

from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Provide a basic command prompt for the AirBnB clone."""

    prompt = "(hbnb) "
    classes = {"BaseModel": BaseModel}

    def _valid_class(self, args):
        """Check the class name and print the required error if invalid."""
        if not args:
            print("** class name missing **")
            return False
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        return True

    def _find_instance(self, args):
        """Find an instance after checking its class name and ID."""
        if not self._valid_class(args):
            return None
        if len(args) < 2:
            print("** instance id missing **")
            return None
        obj = storage.all().get("{}.{}".format(args[0], args[1]))
        if obj is None:
            print("** no instance found **")
        return obj

    def do_create(self, arg):
        """Create and save an object: create BaseModel."""
        args = arg.split()
        if self._valid_class(args):
            obj = self.classes[args[0]]()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """Display an object: show BaseModel <id>."""
        obj = self._find_instance(arg.split())
        if obj is not None:
            print(obj)

    def do_destroy(self, arg):
        """Delete and save an object: destroy BaseModel <id>."""
        args = arg.split()
        obj = self._find_instance(args)
        if obj is not None:
            del storage.all()["{}.{}".format(args[0], args[1])]
            storage.save()

    def do_all(self, arg):
        """List all objects, optionally filtered: all [BaseModel]."""
        args = arg.split()
        if args and not self._valid_class(args):
            return
        objects = []
        for obj in storage.all().values():
            if not args or obj.__class__.__name__ == args[0]:
                objects.append(str(obj))
        print(objects)

    def do_update(self, arg):
        """Save one attribute: update BaseModel <id> <attribute> <value>."""
        args = shlex.split(arg)
        obj = self._find_instance(args)
        if obj is None:
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        name = args[2]
        if name in ("id", "created_at", "updated_at"):
            return
        value_type = type(getattr(obj, name, ""))
        setattr(obj, name, value_type(args[3]))
        obj.save()

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
