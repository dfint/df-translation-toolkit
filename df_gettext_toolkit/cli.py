import typer

import df_gettext_toolkit.convert as convert

app = typer.Typer()
app.add_typer(convert.cli.app, name="convert")
