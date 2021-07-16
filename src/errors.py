class CommandNotFound(Exception):
    """Command not found"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnknownCommand(Exception):
    """Unknow command"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnknownOption(Exception):
    """Unknown Option"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidOption(Exception):
    """Invalid Option"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidSyntax(Exception):
    """Invalid Syntax"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
