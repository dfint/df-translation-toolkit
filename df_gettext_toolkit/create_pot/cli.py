import typer

from df_gettext_toolkit.create_pot import from_string_dump, from_steam_text

app = typer.Typer()
app.command(name="from_string_dump")(from_string_dump.main)
app.command(name="from_steam_text")(from_steam_text.main)
