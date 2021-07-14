from __future__ import annotations

from typing import Callable


class Command:
    """Base class for commands"""

    commands: list[Command] = []

    def __init__(self,
                 name: str,
                 terminal: None,
                 options: list[list[str], list[str]],
                 func: Callable[[None, dict[str, str], list[str]], None],
                 parent: Command | str = None) -> None:
        """Creates a Command to use in `Terminal`

        Args:
            name (str): The name of the command
            terminal (Terminal): The terminal this command belongs to
            options (list[list[str], list[str]]): Valid options for command
            func (Callable[[None, dict[str, str], list[str]], None]): The Function to call when command is run
            parent (Command, optional): the parent this command belongs to. Defaults to None.
        """
        self.name = name
        self.terminal = terminal
        self.options = options
        self.func = func
        self.parent = parent
        if self.parent is not None:
            if type(self.parent) == str:
                for _command in Command.commands:
                    if _command.name == self.parent:
                        self.parent = _command
                        break
                else:
                    self.terminal.console.print("Parent command Not Found!")
                    raise KeyboardInterrupt
            self.parent.add_subcommand(self)
        self._subcommands: list[Command] = []
        Command.commands.append(self)

    def add_subcommand(self, subcommand: Command | str) -> None:
        """Adds a subcommand to a already existing command

        Args:
            child (Command): The subcommand to add
        """
        if subcommand is str:
            for command in Command.commands:
                if command.name == subcommand:
                    self._subcommands.append(command)

        self._subcommands.append(subcommand)

    @classmethod
    def is_command(cls, command: Command | str) -> bool:
        """Check if the given command exists

        Args:
            command (Command | str): The command to check

        Returns:
            bool: `True` if Exists else `False`
        """
        for _command in cls.commands:
            if _command.name == command or _command == command:
                return True
        return False

    @classmethod
    def get_command(cls, command: str) -> Command:
        """Return `Command` object from command name

        Args:
            command (str): Name of the command "as of `command.name`"

        Returns:
            Command: The `Command` object if exists else `None`
        """
        for _command in cls.commands:
            if _command.name == command:
                return _command
        return None

    @classmethod
    def has_subcommands(cls, command: str | Command) -> bool:
        """Checks if a command has subcommand/s

        Args:
            command (str|Command): The Command

        Returns:
            bool: True if `command` has subcommand/s else False
        """
        for _command in cls.commands:
            if _command.name == command or _command == command:
                return _command._subcommands != []

    @classmethod
    def is_subcommand(cls, subcommand: str | Command, command: str | Command) -> bool:
        """Check if the given command is sub command of one

        Args:
            subcommand (str|Command): The Subcommand
            command (str|Command): The Command

        Returns:
            bool: True if it is a Subcommand else False
        """
        for _command in cls.commands:
            if _command.name == command or _command == command:
                for _subcommand in _command._subcommands:
                    if subcommand == _subcommand.name or subcommand == _subcommand:
                        return True
        return False

    @classmethod
    def get_all_commands(cls) -> list[Command]:
        """Returns all available commands

        Returns:
            list[Command]: A list of `Command` object
        """
        return cls.commands

    def run(self, options: dict[str, str], params: list[str]) -> None:
        """Runs the command

        Args:
            options (dict[str, str]): Options from input, ex. `-V` or `--help`
            params (list[str]): Parameter from input
        """
        _options: list[list[str], dict[str, str]] = [[], {}]
        for key, value in options.items():
            if key.startswith("--") and key in self.options[1]:
                _options[1][key] = value
            elif key.startswith("-") and key in self.options[0]:
                _options[0].append(key)
            else:
                self.terminal.console.print(f"Unknown option: {key}")
                return

        self.func(self.terminal, _options, params)


def _test(terminal: None, options: list[list[str], dict[str, str]], params: list[str]) -> None:
    """Test func"""
    terminal.console.print(f"Hello: option: {options}\nparams: {params}")


def _test1(terminal: None, options: dict[str, str], params: list[str]) -> None:
    """Test func1"""
    terminal.console.print(f"World: option: {options}\nparams: {params}")


def init(terminal: None) -> None:
    """Initialize the command module and create commands

    Args:
        terminal (Terminal): The `Terminal` object to add commands to
    """
    Command("test", terminal, [["-v"], ["--me"]], _test)
    Command("test1", terminal, [["-v"], ["--me"]], _test1, "test")
    for command in Command.commands:
        terminal.commands.append(command)
