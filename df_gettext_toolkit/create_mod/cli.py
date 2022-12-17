import typer

from df_gettext_toolkit.create_mod import from_vanilla

app = typer.Typer()
app.command(name="from_vanilla")(from_vanilla.main)
