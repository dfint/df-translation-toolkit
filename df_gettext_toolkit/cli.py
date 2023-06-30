import typer

import df_gettext_toolkit.convert as convert
from df_gettext_toolkit import create_pot

commands = [
    ("convert", convert.cli.app),
    ("create_pot", create_pot.cli.app),
]

app = typer.Typer()

for command in commands:
    app.add_typer(command[1], name=command[0])
