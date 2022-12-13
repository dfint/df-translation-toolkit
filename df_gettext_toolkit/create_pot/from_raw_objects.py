from pathlib import Path
from typing import Iterator, TextIO

import typer

from df_gettext_toolkit.parse.parse_po import save_pot
from df_gettext_toolkit.parse.parse_raws import extract_translatables_from_raws
from df_gettext_toolkit.utils.common import TranslationItem


def extract_from_raw_file(file_name: Path, source_encoding: str) -> Iterator[TranslationItem]:
    with open(file_name, encoding=source_encoding) as file:
        for item in extract_translatables_from_raws(file):
            item.source_file = file_name.name
            yield item


def extract_translatables_from_raws_batch(raw_files: Iterator[Path], source_encoding: str) -> Iterator[TranslationItem]:
    """
    Read all translatable items from all raw files
    """
    for file_name in raw_files:
        if file_name.is_file():
            yield from extract_from_raw_file(file_name, source_encoding)


def create_pot_file(pot_file: TextIO, raw_files: Iterator[Path], source_encoding: str):
    save_pot(
        pot_file,
        extract_translatables_from_raws_batch(raw_files, source_encoding),
    )


def main(raws_path: Path, pot_file: typer.FileTextWrite, source_encoding: str = "cp437"):
    raw_files = (file for file in raws_path.glob("*.txt") if not file.name.startswith("language_"))
    create_pot_file(pot_file, sorted(raw_files), source_encoding)


if __name__ == "__main__":
    typer.run(main)
