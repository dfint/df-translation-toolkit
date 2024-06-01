import typer

from df_translation_toolkit import convert, create_pot

app = typer.Typer()
app.add_typer(convert.cli.app, name="convert")
app.add_typer(create_pot.cli.app, name="create_pot")
