from __future__ import annotations

import os
import hashlib
import datetime
import pathlib
import shutil
from typing import Callable, List
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

class CommandNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidID(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Command:

    top_commands = []
    top_command_ids = []
    command_ids = []
    commands = []

    def __init__(self, name: str, parent: int | None, subcommands: List[int] | None, id: int, func: Callable) -> None:
        self.name = name
        self.parent = parent
        self.id = id
        self.func = func
        self.arguments = None

        if self.parent is not None:
            if not self.is_command(self.parent):
                raise CommandNotFound

        self.subcommands = subcommands
        if self.subcommands is not None:
            for x in self.subcommands:
                if not self.is_command(x):
                    raise CommandNotFound
        
        if self.id not in Command.command_ids:
            if self.parent is None:
                Command.top_command_ids.append(self.id)
                Command.top_commands.append(self)
            Command.command_ids.append(self.id)
            Command.commands.append(self)
        else:
            raise InvalidID
        
    def run(self, info: list) -> str:
        self.arguments = info
        answer = self.func(*self.arguments)
        return answer
    
    @classmethod
    def is_command(self, command_id: int) -> bool:
        if command_id in Command.command_ids:
            return True
        else:
            return False

    @classmethod
    def get_command_from_id(self, command_id: int) -> Command:
        
        if self.is_command(command_id):
            index = Command.command_ids.index(command_id)
            return Command.commands[index]
        else:
            raise CommandNotFound
    
    @classmethod
    def get_command_from_name(self, command_name: str) -> Command:
        for x in Command.commands:
            if x.name == command_name:
                return x
        raise CommandNotFound
    
    @classmethod
    def is_command_from_name(self, command) -> bool:
        try:
            self.get_command_from_name(command)
            return True
        except CommandNotFound:
            return False
    

class File:
    def __init__(self, path) -> None:
        self.path = path
        self.extension = os.path.splitext(self.name)[-1]
        self.info = pathlib.Path(self.path)

    def rename(self) -> None:
        os.rename(self.path)

    def run(self):
        os.startfile(self.path)
    
    def delete(self):
        os.remove(self.path)
        del self
    
    def get_checksum(self, file_name: str) -> str:
        """Returns checksum of the file"""
        sha_hash = hashlib.sha224()
        a_file = open(file_name, "rb")
        content = a_file.read()
        sha_hash.update(content)
        digest = sha_hash.hexdigest()
        a_file.close()
        return digest
    
    def get_last_modified_time(self) -> datetime.datetime:
        """Returns last modified time as datetime.datetime object"""
        return datetime.datetime.fromtimestamp(self.info.stat().st_mtime)

    def get_created_time(self) -> datetime.datetime:
        """Returns created time as datetime.datetime object"""
        return datetime.datetime.fromtimestamp(self.info.stat().st_ctime)

class Directory:
    def __init__(self, path) -> None:
        self.path = path
        self.info = pathlib.Path(self.path)

        # [TODO] Parse the files and directories
        self.files, self.directories = [], []

    def get_last_modified_time(self) -> datetime.datetime:
        """Returns last modified time as datetime.datetime object"""
        return datetime.datetime.fromtimestamp(self.info.stat().st_mtime)

    def get_created_time(self) -> datetime.datetime:
        """Returns created time as datetime.datetime object"""
        return datetime.datetime.fromtimestamp(self.info.stat().st_ctime)

    def delete(self) -> None:
        shutil.rmtree(self.path)
        del self

class Terminal:
    def __init__(self) -> None:
        self.path = Directory(pathlib.Path().absolute())
        self.commands = {

        }
    
    def parse(self, inp) -> str:

        # [TODO] This is to be done.
        # The way to do this is to check whether the first one is a top command (Command.top_commands)
        # And then check whether the rest are subcommands of each other.
        # Note that the only way you can do this is by equating the ID - I did this for simplicity.
        # You can get commands from self.commands. 
        # You also need to seperate the arguments from the commands.
        ...

def render(console: Console) -> None:
    """Renders a main menu

    Args:
        console (Console): Console to print on
    """
    console.print(Rule("[bold blue]CLI File Manager", style="red"))
    console.print(Panel("[white]Welcome to The [bold]BETTER[/bold] File manager\nFor help type: `help` or `h`",
                        style="green"))

terminal_engine = Terminal()
terminal = Console(highlight=False)
render(terminal)


while True:
    try:
        inp = terminal.input(f"{terminal_engine.path.path}❯❯ ")
        parsed = terminal_engine.parse(inp)
        if parsed is None:
            terminal.print("")
        else:
            terminal.print(parsed)
    except (KeyboardInterrupt, EOFError):
        terminal.clear()
        terminal.print("[red bold]Thanks for using This app :-)")
        break
    except Exception as e:
        terminal.print(f"[red]{str(e)}")
