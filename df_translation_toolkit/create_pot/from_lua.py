from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import BinaryIO

import typer

from df_translation_toolkit.parse.parse_lua import extract_translatables_from_lua_file
from df_translation_toolkit.utils.po_utils import TranslationItem, save_pot


def extract_from_file(base_path: Path, file_name: Path, source_encoding: str) -> Iterator[TranslationItem]:
    with file_name.open(encoding=source_encoding) as file:
        for item in extract_translatables_from_lua_file(file):
            item.source_file = str(file_name.relative_to(base_path))
            yield item


SKIP_FILES = {"language.lua"}


def extract_translatables_batch(
    base_path: Path,
    files: Iterable[Path],
    source_encoding: str,
) -> Iterator[TranslationItem]:
    """
    Read all translatable items from files
    """
    for file_name in files:
        if file_name.is_file() and file_name.name not in SKIP_FILES:
            yield from extract_from_file(base_path, file_name, source_encoding)


def create_pot_file(base_path: Path, pot_file: BinaryIO, raw_files: Iterable[Path], source_encoding: str) -> None:
    save_pot(
        pot_file,
        extract_translatables_batch(base_path, raw_files, source_encoding),
    )


def main(game_path: Path, pot_file: typer.FileBinaryWrite, source_encoding: str = "cp437") -> None:
    lua_file_path = game_path / "data"
    lua_files = (file for file in lua_file_path.rglob("*.lua"))
    create_pot_file(game_path, pot_file, sorted(lua_files), source_encoding)


if __name__ == "__main__":
    typer.run(main)
