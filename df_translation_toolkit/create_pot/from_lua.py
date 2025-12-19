from pathlib import Path

import typer

from df_translation_toolkit.parse.parse_lua import parse_lua_file


def main(game_path: Path, pot_file: typer.FileBinaryWrite, source_encoding: str = "cp437") -> None:
    lua_file_path = game_path / "data/vanilla/vanilla_procedural/scripts"
    lua_files = (file for file in lua_file_path.rglob("*.lua"))
    print(list(lua_files))


if __name__ == "__main__":
    typer.run(main)
