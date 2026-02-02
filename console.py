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

    def do_all(self, arg):
        """Print all objects, optionally filtered by class."""
        tokens = shlex.split(arg)
        if len(tokens) == 0:
            objs = storage.all()
        else:
            class_name = tokens[0]
            cls = classes.get(class_name)
            if cls is None:
                print("** class doesn't exist **")
                return
            objs = storage.all(cls)
        print([str(v) for v in objs.values()])

    def do_show(self, arg):
        """Show an instance by class name and id."""
        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** class name missing **")
            return
        class_name = tokens[0]
        cls = classes.get(class_name)
        if cls is None:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
            return
        obj_id = tokens[1]
        key = "{}.{}".format(class_name, obj_id)
        objs = storage.all(cls)
        if key not in objs:
            print("** no instance found **")
            return
        print(objs[key])

    def do_destroy(self, arg):
        """Destroy an instance by class name and id."""
        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** class name missing **")
            return
        class_name = tokens[0]
        cls = classes.get(class_name)
        if cls is None:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
            return
        obj_id = tokens[1]
        key = "{}.{}".format(class_name, obj_id)
        objs = storage.all(cls)
        if key not in objs:
            print("** no instance found **")
            return
        obj = objs[key]
        storage.delete(obj)
        storage.save()
        print()

    def do_update(self, arg):
        """Update an instance by class name, id, attribute name and value."""
        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** class name missing **")
            return
        class_name = tokens[0]
        cls = classes.get(class_name)
        if cls is None:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
            return
        obj_id = tokens[1]
        key = "{}.{}".format(class_name, obj_id)
        objs = storage.all(cls)
        if key not in objs:
            print("** no instance found **")
            return
        if len(tokens) < 3:
            print("** attribute name missing **")
            return
        if len(tokens) < 4:
            print("** value missing **")
            return
        attr_name = tokens[2]
        attr_value = tokens[3]
        if attr_name in ("id", "created_at", "updated_at"):
            return
        obj = objs[key]
        try:
            setattr(obj, attr_name, int(attr_value))
        except ValueError:
            try:
                setattr(obj, attr_name, float(attr_value))
            except ValueError:
                setattr(obj, attr_name, attr_value.strip('"'))
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
