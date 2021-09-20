from typing import List
from ..parsers.baseparser import BaseParser
from ..misc import Style
import colorama

colorama.init()


class BaseLoop:
    def __init__(
        self, parser: BaseParser, style: Style = Style(), histsize: int = 100
    ) -> None:

        self._histfile: List[str] = []
        self.histsize: int = histsize
        self.histindex: int = 0
        self.parser: BaseParser = parser
        self.style: Style = style

    def handle_errors(self, error: Exception) -> str:
        exception_name = error.__class__.__name__
        exception_value = str(error)
        error_string = f"{self.style.error_name}{exception_name}"
        error_string += f"{self.style.reset}"

        if len(exception_value) != 0:
            error_string += (
                f": {self.style.error_message}{exception_value}"
                + f"{self.style.reset}"
            )

        return error_string

    def handle_success(self, output: str) -> str:
        return f"{self.style.success_colour}{output}{self.style.reset}"

    def parse_run(self, input_string: str) -> str:

        self.add_to_histfile(input_string)
        try:
            returned_value = self.parser.parse_run(input_string)
            return self.handle_success(returned_value)
        except Exception as error:
            return self.handle_errors(error)

    def add_to_histfile(self, inp: str) -> None:

        if len(self._histfile) < self.histsize:
            self._histfile.append(inp)
        elif len(self._histfile) == self.histsize:
            self._histfile.pop(0)
            self._histfile.append(inp)

        self.histindex = len(self._histfile) - 1

    def clear_histfile(self) -> None:
        self._histfile = []

    def read_histfile_up(self) -> str:
        if self.histindex != 0:
            self.histindex -= 1
        else:
            self.histindex = 0
        return self._histfile[self.histindex]

    def read_histfile_down(self) -> str:
        if self.histindex != len(self._histfile) - 1:
            self.histindex += 1
        else:
            self.histindex = 0
        return self._histfile[self.histindex]

    def switch_parser(self, parser: BaseParser) -> None:
        self.parser = parser
