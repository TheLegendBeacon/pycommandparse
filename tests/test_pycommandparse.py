try:
    from pycommandparse import __version__
    from pycommandparse.parsers import BaseParser
    from pycommandparse.errors import CommandNotFound, ArgumentError
    from pycommandparse.event_loops.baseloop import BaseLoop, Style
except ModuleNotFoundError:
    from ..pycommandparse import __version__
    from ..pycommandparse.parsers import BaseParser
    from ..pycommandparse.errors import CommandNotFound, ArgumentError
    from ..pycommandparse.event_loops.baseloop import BaseLoop, Style

import pytest


def test_version():
    assert __version__ == "1.0.0"


def test_base_Baseparser():
    x = BaseParser()

    @x.command(name="add", aliases=["addition", "sum"])
    def add(*numbers) -> str:  # noqa F811
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

    del add

    @x.group(name="group", aliases=["test"])
    def group_func(*args):
        return "no"

    assert x.parse_run("test") == "no"

    group = x.get_group("group")

    @group.command(name="e", aliases=["f"], number_of_arguments=2)
    def e(x, y):
        return "ok and?"

    assert x.parse_run("test e gh it") == "ok and?"

    @x.group(name="math", aliases=["m"])
    def mathfunc(*args):
        return "use the subcommands"

    math = x.get_group("math")

    @math.command(name="add", aliases=["a"], usage="add <numbers>")
    def add(*args):
        return str(sum([int(x) for x in args]))

    assert x.parse_run("m") == "use the subcommands"
    assert x.parse_run("math add 3 5") == "8"
    assert x.parse_run("m a 4 5") == "9"

    print("\u001b[32;1mPASS\u001b[0m")


def test_base_loop():
    parser = BaseParser()

    @parser.command(
        name="say",
        aliases=["print"],
        usage="say <anything>",
        description="Repeats anything you say.",
    )
    def say(*args):
        return " ".join(args)

    loop = BaseLoop(parser, Style.NoStyle())
    assert loop.parse_run("say 3 5 6") == "3 5 6"
