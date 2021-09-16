from typing import Dict
from ..errors import ArgumentError, CommandNotFound
from ..command import Command


class BaseParser:
    def __init__(self, commands: list[Command], histsize: int = 100):
        self._histsize = histsize
        self._histfile = []


        self.commands: dict[str, Command] = {}
        for command in commands:
            self.add_command(command=command)

        self.add_command(Command("help", self.help, description="Provides documentation for commands.", aliases=['h']))
    
    def _add_to_histfile(self, inp: str):
        if len(self._histfile) < self._histsize:
            self._histfile.append(inp)
        elif len(self._histfile) == self._histsize:
            self._histfile.pop(0)
            self._histfile.append(inp)
    
    def _clear_histfile(self):
        self._histfile = []

    def help(self, *args):

        if len(args) > 1:
            raise ArgumentError("Too Many Arguments. Help takes 0 or 1 argument.")

        if len(args) == 0:
            docs = []
            for command in set(self.commands.values()):
                docs.append(f'{command.name}: {command.description}')
            return "\n".join(docs)

        commandName = args[0]
            
        if commandName not in self.commands:
            raise CommandNotFound(f"\"{commandName}\" not found.")

        command = self.commands[commandName]
        docs = f"Function \"{command.name}\"\n\tAliases: {command.aliases}\n\tUsage: {command.usage}\n\tDescription: {command.description}"
        return docs


    def add_command(self, command: Command):
        aliases = command.aliases
        name = command.name
        for x in [name, *aliases]:
            self.commands[x] = command

    def check_commas(self, inputs: list):
        form_inputs = []
        temp_list = []

        inquote = False
        for x in inputs:
            if list(x).count('"') % 2 == 0:
                if not inquote:
                    form_inputs.append(x.replace('"', ''))
                else:
                    temp_list.append(x)
            else:
                if inquote == False:
                    inquote = True
                    temp_list.append(x.replace('"', ''))
                else:
                    temp_list.append(x.replace('"', ''))
                    total_string = " ".join(temp_list)
                    form_inputs.append(total_string)
                    temp_list = []
                    inquote = False
        
        return form_inputs

    def parse(self, inp):
        inputs = inp.split(" ")
        form_inputs = self.check_commas(inputs)

        command = form_inputs[0]

        if command not in self.commands:
            raise CommandNotFound(f"\"{command}\" not found.")

        arguments = form_inputs[1:]

        if self.commands[command].number_of_args is not None:
            if len(arguments) != self.commands[command].number_of_args:
                raise ArgumentError

        self._add_to_histfile(inp)
        return {self.commands[command]: arguments}
    
    def parse_run(self, inp: str):
        parsed = self.parse(inp)
        command = list(parsed.keys())[0]
        return command(*parsed[command])
