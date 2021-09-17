class Command:
    def __init__(
        self,
        name,
        command,
        usage: str = None,
        description: str = "Not Implemented.",
        number_of_args: int = None,
        aliases: list[str] = [],
    ):
        self.name = name
        self.command = command
        self.usage = usage
        if usage == None:
            self.usage = f"{self.name} *args"
        self.description = description
        self.aliases = aliases
        self.number_of_args = number_of_args

    def __call__(self, *args):
        return self.command(*args)
