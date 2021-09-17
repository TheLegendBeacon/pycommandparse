from pycommandparse import __version__
from pycommandparse.parsers import BaseParser as Parser
from pycommandparse import Command

def test_version():
    assert __version__ == '0.1.0'

def test_base_parser():
    x = Parser()

    @x.command(name="add", aliases=['addition', 'sum'])
    def add(*args): 
        intlist = []
        try:
            for x in args:
                intlist.append(int(x))
        except ValueError:
            return "ArgumentError: Unable to turn a value into an integer."
        return str(sum(intlist))

    assert x.parse_run("add 3 5 6") == '14'
    assert x.parse_run("add 3 5 hi") == 'ArgumentError: Unable to turn a value into an integer.'

