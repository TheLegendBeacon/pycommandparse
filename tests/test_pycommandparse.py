from pycommandparse import __version__
from pycommandparse.parsers import BaseParser as Parser
from pycommandparse.errors import CommandNotFound, ArgumentError
import pytest


def test_version():
    assert __version__ == "0.1.0"


def test_base_parser():
    x = Parser()

    @x.command(name="add", aliases=["addition", "sum"])
    def add(*numbers):
        intlist = []
        try:
            for x in numbers:
                intlist.append(int(x))
        except ValueError:
            raise ArgumentError("Unable to turn a value into an integer.")
        return str(sum(intlist))

    assert x.parse_run("add 3 5 6") == "14"
    with pytest.raises(ArgumentError):
        x.parse_run("add 3 6 76 hi")

    x.remove_command(x.get_command("add"))

    with pytest.raises(CommandNotFound):
        x.parse_run("add 3 5 6")
