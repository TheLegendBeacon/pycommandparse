# Pycommandparse
## Structure
In pycommandparse, each function is bound to a `pycommandparse.Command` instance.
The Parser takes these as inputs.

Internally, the parser has a dictionary with keys having all names and aliases with the values being the corresponding `Command` instances.

The Parser matches the imcoming commands to the given names/aliases and runs the command with the arguments.

## Examples


### Defining and Adding Commands

Method 1: Directly defining the command.

```py
from pycommandparse.parsers import BaseParser

parser = BaseParser()

# Ways to define commands

## 1. directly via pycommandparse.Command
from pycommandparse import Command

def mult(x, y):
    return int(x)*int(y)

multiplication = Command(name="multiply", 
                    command=mult, 
                    usage="multiply *args", description="Multiplies 2 numbers you input", 
                    number_of_args=2, 
                    aliases=['product'])

parser.add_command(multiplication)

parser.parse_run("multiply 3 5") # Outputs "15"
```

Method 2: Decorators.

```py
from pycommandparse.parsers import BaseParser


## 2. Using decorator

### Not specifying number_of_args will allow any number of arguments.

@parser.command(name="add", 
            aliases=['sum'], 
            usage="add *numbers", 
            description="Adds what you input.")
def add(*numbers):
    return sum([int(number) for number in numbers])

parser.parse_run("add 3 5 6 7") # Outputs "21"
parser.parse_run("add 2 4") # Outputs "6"
```