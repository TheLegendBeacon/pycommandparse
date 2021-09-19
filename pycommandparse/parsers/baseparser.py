from typing import Dict, List, Any
from ..errors import ArgumentError, CommandNotFound, GroupNotFound
from ..command import Command, Group


def check_commas(inputs: list):
    form_inputs = []
    temp_list = []

    inquote = False
    for x in inputs:
        if list(x).count('"') % 2 == 0:
            if not inquote:
                form_inputs.append(x.replace('"', ""))
            else:
                temp_list.append(x)
        else:
            if inquote == False:
                inquote = True
                temp_list.append(x.replace('"', ""))
            else:
                temp_list.append(x.replace('"', ""))
                total_string = " ".join(temp_list)
                form_inputs.append(total_string)
                temp_list = []
                inquote = False

    return form_inputs


class BaseParser(Group):
    def __init__(
        self,
        commands: List[Command] = [],
        groups: List[Group] = [],
        histsize: int = 100,
    ) -> None:
        Group.__init__(self, name="__parser__", commands=commands)
        self._histfile = []
        self._histsize = histsize
        self.groups: List[Group] = [self]
        self.commands = [x for x in self]
        self.group_dict: Dict[str, Group] = {None: self}

        for group in groups:
            self.add_group(group)

    def get_group(self, groupName: str):
        if groupName not in self.group_dict:
            raise GroupNotFound
        return self.group_dict[groupName]

    def add_group(self, group: Group):
        self.groups.append(group)
        aliases = group.aliases
        name = group.name
        for x in [name, *aliases]:
            self.group_dict[x] = group

    def remove_group(self, group: Group):
        self.groups.remove(group)
        for key, val in zip(
            list(self.group_dict.keys()), list(self.group_dict.values())
        ):
            if val == group:
                del self.command_dict[key]

    def parse(self, inp: str) -> Dict[Command, List]:
        print(inp)
        inputs = inp.split(" ")
        form_inputs = check_commas(inputs)
        command = form_inputs[0]
        arguments = form_inputs[1:]

        if command in self.command_dict:

            if self.command_dict[command].number_of_args is not None:

                if len(arguments) != self.command_dict[command].number_of_args:
                    raise ArgumentError

            self._add_to_histfile(inp)
            return {self.command_dict[command]: arguments}

        elif command in self.group_dict:
            group = self.group_dict[command]
            self._add_to_histfile(inp)
            return group.parse(*arguments)

        else:
            raise CommandNotFound

    def parse_run(self, inp: str) -> Any:
        parsed = self.parse(inp)
        command = list(parsed.keys())[0]
        return command(*parsed[command])

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

    def group(
        self,
        name: str,
        aliases: list = [],
        description: str = "No description.",
    ):
        def decorator(function):
            fallback = Command(
                name,
                function,
                description,
                aliases=aliases,
            )
            self.add_group(
                Group(name, fallback, description=description, aliases=aliases)
            )

        return decorator

    def _add_to_histfile(self, inp: str):
        if len(self._histfile) < self._histsize:
            self._histfile.append(inp)
        elif len(self._histfile) == self._histsize:
            self._histfile.pop(0)
            self._histfile.append(inp)

    def _clear_histfile(self):
        self._histfile = []
