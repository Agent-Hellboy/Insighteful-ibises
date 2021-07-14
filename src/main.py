from shlex import split

from rich.console import Console

from src import command
from src.command import Command
from templates import main_menu


class Terminal:
    """The main Application class that handles everything"""

    def __init__(self) -> None:
        self.console = Console()
        self.running = False
        self.commands = []
        self.NO_PARAM_OPTIONS = [
            '-v'
        ]
        command.init(self)

    def parse_input(self, input: str) -> tuple:
        """A helper method to parse out input to command attributes and stuff

        Args:
            input (str): The plain str input

        Returns:
            tuple: parsed strings
        """
        try:
            words = split(input)
        except ValueError:
            return {"error": [0, input]}
        _command = [words[0]]
        words.pop(0)
        _options = {}
        _params = []
        while Command.has_subcommands(_command[-1]) and words != []:
            if Command.is_subcommand(words[0], _command[-1]):
                _command.append(words[0])
                words.pop(0)
                continue
            break
        for i, word in enumerate(words):
            if word.startswith("--"):
                if len(_params) != 0:
                    return {"error": [1, input]}
                if len(words) - 1 != i:
                    _options[word] = words[i + 1]
                    words.pop(i+1)
                else:
                    _options[word] = ""
            elif word.startswith("-"):
                if len(_params) != 0:
                    return {"error": [2, input]}
                if len(word) > 2:
                    _options[word[0:2]] = ""
                    _params.append(word[2:])
                else:
                    _options[word] = ""
            else:
                _params.append(word)

        return _command, _options, _params

    def run_command(self, data: tuple) -> None:
        """Runs the corresponding Command using the data

        Args:
            data (tuple): The data in three parts: Command, options, params
        """
        command = Command.get_command(data[0][-1])
        if command is not None:
            command.run(data[1], data[2])
            return
        s = " "
        self.console.print(f"Unknown Command:{s.join(data[0])}")

    def run(self) -> None:
        """Main function that starts the application"""
        main_menu.render(self.console)
        self.running = True
        while self.running:
            input = self.console.input("> ")
            self.run_command(self.parse_input(input))
