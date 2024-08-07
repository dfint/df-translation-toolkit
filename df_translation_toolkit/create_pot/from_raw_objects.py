from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import BinaryIO

import typer

from df_translation_toolkit.parse.parse_raws import extract_translatables_from_raws
from df_translation_toolkit.utils.po_utils import TranslationItem, save_pot


def extract_from_raw_file(file_name: Path, source_encoding: str) -> Iterator[TranslationItem]:
    with file_name.open(encoding=source_encoding) as file:
        for item in extract_translatables_from_raws(file):
            item.source_file = file_name.name
            yield item


def extract_translatables_from_raws_batch(raw_files: Iterable[Path], source_encoding: str) -> Iterator[TranslationItem]:
    """
    Read all translatable items from all raw files
    """
    for file_name in raw_files:
        if file_name.is_file():
            yield from extract_from_raw_file(file_name, source_encoding)


def create_pot_file(pot_file: BinaryIO, raw_files: Iterable[Path], source_encoding: str) -> None:
    save_pot(
        pot_file,
        extract_translatables_from_raws_batch(raw_files, source_encoding),
    )


def main(raws_path: Path, pot_file: typer.FileBinaryWrite, source_encoding: str = "cp437") -> None:
    raw_files = (file for file in raws_path.glob("*.txt") if not file.name.startswith("language_"))
    create_pot_file(pot_file, sorted(raw_files), source_encoding)


if __name__ == "__main__":
    typer.run(main)
