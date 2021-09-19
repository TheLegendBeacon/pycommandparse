from typing import Any, Callable, Dict, List, Optional
from .errors import CommandNotFound, ArgumentError


class MetaData:
    def __init__(
        self,
        name: str,
        description: Optional[str] = "Not Implemented.",
        aliases: List[str] = [],
    ) -> None:
        self.name = name
        self.description = description
        self.aliases = aliases


class Command(MetaData):
    def __init__(
        self,
        name: str,
        command: Callable[..., str],
        usage: Optional[str] = None,
        description: Optional[str] = "Not Implemented.",
        number_of_args: Optional[int] = None,
        aliases: List[str] = [],
    ) -> None:

        MetaData.__init__(self, name, description, aliases)
        self.usage = usage
        self.command: Callable[..., str] = command
        self.number_of_args: Optional[int] = number_of_args

        if usage == None:
            self.usage = f"{self.name} *args"

    def __call__(self, *args) -> Any:
        return self.command(*args)


class Group(MetaData):
    def __init__(
        self,
        name: str,
        fallbackFunction=Command,
        commands: List[Command] = [],
        description: Optional[str] = "No Description.",
        aliases: List[str] = [],
    ) -> None:
        MetaData.__init__(self, name, description, aliases)
        self.fallback = fallbackFunction
        self.commands = []
        self.command_dict: Dict[str, Command] = {}
        for command in commands:
            self.add_command(command)

    def get_command(self, commandName: str) -> None:
        if commandName not in self.command_dict:
            raise CommandNotFound
        return self.command_dict[commandName]

    def add_command(self, command: Command) -> None:
        self.commands.append(command)
        aliases = command.aliases
        name = command.name
        for x in [name, *aliases]:
            self.command_dict[x] = command

    def remove_command(self, command: Command) -> None:
        self.commands.remove(command)
        for key, val in zip(
            list(self.command_dict.keys()), list(self.command_dict.values())
        ):
            if val == command:
                del self.command_dict[key]

    def command(
        self,
        name: str,
        aliases: list = [],
        usage: str = None,
        description: str = "No description.",
        number_of_arguments: int = None,
    ):
        def decorator(function):
            command = Command(
                name,
                function,
                usage,
                description,
                number_of_args=number_of_arguments,
                aliases=aliases,
            )
            self.add_command(command)

        return decorator

    def parse(self, *args: str) -> Dict[Command, List]:
        if len(args) == 0:
            return {self.fallback: []}

        command = args[0]

        arguments = args[1:]

        if command not in self.command_dict:
            raise CommandNotFound

        if self.command_dict[command].number_of_args is not None:

            if len(arguments) != self.command_dict[command].number_of_args:
                raise ArgumentError

        return {self.command_dict[command]: arguments}

    def __iter__(self):
        return self.commands.__iter__()

    def __next__(self):
        try:
            return self.commands.__next__()
        except StopIteration:
            raise StopIteration
