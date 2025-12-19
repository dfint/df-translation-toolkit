import typer

from df_translation_toolkit.create_pot import from_lua, from_steam_text, from_string_dump

app = typer.Typer()
app.command(name="from_string_dump")(from_string_dump.main)
app.command(name="from_steam_text")(from_steam_text.main)
app.command(name="from_lua")(from_lua.main)
