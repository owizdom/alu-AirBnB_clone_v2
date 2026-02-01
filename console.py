#!/usr/bin/python3
"""HBNB console"""
import cmd
import shlex
import re

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}


def _parse_kv(token):
    """Parse a key=value token according to project rules."""
    if "=" not in token:
        return None
    key, value = token.split("=", 1)
    if not key:
        return None

    # String: starts with a double quote and ends with a double quote
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        inner = value[1:-1]
        inner = inner.replace(r'\"', '"')
        inner = inner.replace("_", " ")
        return key, inner

    # Float: contains a dot and is numeric
    if re.fullmatch(r"-?\d+\.\d+", value):
        try:
            return key, float(value)
        except ValueError:
            return None

    # Integer: default numeric case
    if re.fullmatch(r"-?\d+", value):
        try:
            return key, int(value)
        except ValueError:
            return None

    return None


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def emptyline(self):
        return False

    def do_quit(self, arg):
        return True

    def do_EOF(self, arg):
        print()
        return True

    def do_create(self, arg):
        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** class name missing **")
            return
        class_name = tokens[0]
        cls = classes.get(class_name)
        if cls is None:
            print("** class doesn't exist **")
            return

        kwargs = {}
        for t in tokens[1:]:
            parsed = _parse_kv(t)
            if parsed is None:
                continue
            k, v = parsed
            kwargs[k] = v

        obj = cls(**kwargs)
        obj.save()
        print(obj.id)

    # NOTE: other commands are expected to exist in the original codebase.
    # This patch focuses on task 2 (do_create improvements).


if __name__ == "__main__":
    HBNBCommand().cmdloop()
