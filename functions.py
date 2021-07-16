from prettytable import PrettyTable
from getpass import getuser

def whereami(*args):
    return args[0]

def whoami(*args):
    return getuser()

# Args: required dir, func
def cd(*args):
    args[1](args[0])
    return f"Changed Directory to {args[0]}"

# Args: Column, key
def ls(*args):
    table = PrettyTable()
    table.add_column(fieldname="Items", column=args[0])
    for x in args[1]:
        ... # [TODO]