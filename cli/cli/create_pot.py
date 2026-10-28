from pathlib import Path

import typer

from df_translation_toolkit.create_pot import from_lua, from_raw_objects, from_speech, from_steam_text, from_string_dump

app = typer.Typer()
app.command(name="from_steam_text")(from_steam_text.main)


@app.command(name="from_string_dump")
def from_string_dump_command(
    source_file: typer.FileText,
    destination_file: typer.FileBinaryWrite,
    no_ignore: bool = False,  # noqa: FBT001, FBT002
) -> None:
    from_string_dump.main(source_file, destination_file, no_ignore)


@app.command(name="from_lua")
def from_lua_command(
    game_path: Path,
    pot_file: typer.FileBinaryWrite,
    source_encoding: str = "cp437",
) -> None:
    from_lua.main(game_path, pot_file, source_encoding)


@app.command(name="from_raw_objects")
def from_raw_objects_command(
    raws_path: Path,
    pot_file: typer.FileBinaryWrite,
    source_encoding: str = "cp437",
) -> None:
    from_raw_objects.main(raws_path, pot_file, source_encoding)


@app.command(name="from_speech")
def from_speech_command(path: Path, pot_file: typer.FileBinaryWrite) -> None:
    from_speech.main(path, pot_file)
