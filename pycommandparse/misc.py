from typing import Any, Callable, List, Optional
import colorama


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

        if usage is None:
            self.usage = f"{self.name} *args"

    def __call__(self, *args) -> Any:
        return self.command(*args)


class Style:
    def __init__(self) -> None:
        self.error_name = colorama.Fore.RED
        self.error_message = colorama.Fore.LIGHTYELLOW_EX
        self.success_colour = colorama.Fore.LIGHTWHITE_EX
        self.reset = colorama.Fore.RESET

    @classmethod
    def NoStyle(self):
        style = Style()
        style.error_name = ""
        style.error_message = ""
        style.success_colour = ""
        style.reset = ""
        return style
