# in this file we can do some pre run stuff like initializing the file manager or whatnot
from src import main

app = main.Terminal()
try:
    app.run()
except KeyboardInterrupt:
    app.console.clear()
    app.console.print("[red bold]Thanks for using This app :-)")
