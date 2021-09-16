from pycommandparse import __version__
from pycommandparse.parsers import BaseParser as Parser
from pycommandparse import Command

def test_version():
    assert __version__ == '0.1.0'

def test_base_parser():
    def add(*args): return str(sum([int(x) for x in args]))
    def say(*args): print(*args)

    x = Parser([Command("say", print, description="Says what you ask it to say", aliases=['print'])])
    while True:
        inp = input("❯ ")
        if inp.strip() == "":
            continue
        out = x.parse_run(inp)
        if out is not None:
            print(out)
