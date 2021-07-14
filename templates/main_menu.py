from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule


def render(console: Console) -> None:
    """Renders a main menu

    Args:
        console (Console): Console to print on
    """
    console.print(Rule("[bold blue]CLI File Manager", style="red"))
    console.print(Panel("[white]Welcome to The [bold]BETTER[/bold] File manager\nFor help type: `help` or `h`",
                        style="green"))
