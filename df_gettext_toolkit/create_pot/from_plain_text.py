import sys
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import typer

from df_gettext_toolkit.parse.parse_plain_text import parse_plain_text_file
from df_gettext_toolkit.utils.po_utils import TranslationItem, save_pot


def extract_translatables_from_file(file, file_path, join_paragraphs, keys):
    for text_block, is_translatable, line_number in parse_plain_text_file(file, join_paragraphs):
        if is_translatable:
            if text_block in keys:
                print("Key already exists:", repr(text_block), file=sys.stderr)
            else:
                keys.add(text_block)
                yield TranslationItem(text=text_block.rstrip("\n"), source_file=file_path.name, line_number=line_number)


def extract_translatables(files: Iterable[Path], join_paragraphs: bool) -> Iterator[TranslationItem]:
    keys = set()
    for file_path in files:
        if file_path.is_file():
            print(file_path, file=sys.stderr)
            with open(file_path) as file:
                yield from extract_translatables_from_file(file, file_path, join_paragraphs, keys)


def create_pot_file(pot_file: typer.FileTextWrite, files: Sequence[Path], join_paragraphs: bool):
    save_pot(
        pot_file,
        extract_translatables(files, join_paragraphs),
    )


def main(path: Path, pot_file: typer.FileTextWrite = typer.Option(..., encoding="utf-8"), split: bool = True):
    files = (file for file in path.rglob("*.txt") if file.is_file())
    create_pot_file(pot_file, sorted(files), not split)


if __name__ == "__main__":
    typer.run(main)
