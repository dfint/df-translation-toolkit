import sys
from collections.abc import Mapping
from pathlib import Path

import typer
from babel.messages.pofile import read_po

from df_translation_toolkit.parse.parse_plain_text import parse_plain_text_file
from df_translation_toolkit.utils.backup import backup


def translate_plain_text_file(
    source_file_path: Path,
    destination_file_path: Path,
    dictionary: Mapping[str, str],
    encoding: str,
    join_paragraphs: bool,
):
    with source_file_path.open() as source_file:
        with destination_file_path.open("w", encoding=encoding) as destination_file:
            yield destination_file_path.name
            for text_block, is_translatable, _ in parse_plain_text_file(source_file, join_paragraphs):
                text_block = text_block.rstrip("\n")
                if text_block in dictionary:
                    translation = dictionary[text_block]
                    if not translation:
                        translation = text_block
                else:
                    translation = text_block
                print(translation, file=destination_file)


def translate_plain_text(po_filename: Path, path: Path, encoding: str, join_paragraphs=True):
    with po_filename.open("r", encoding="utf-8") as po_file:
        dictionary = {item.id: item.string for item in read_po(po_file) if item.id}

    for path in Path(path).rglob("*.txt"):
        if path.is_file():
            with backup(path) as backup_file:
                yield from translate_plain_text_file(backup_file, path, dictionary, encoding, join_paragraphs)


def main(
    po_filename: Path,
    path: Path,
    encoding: str,
    split: bool = False,
):
    join_paragraphs = not split
    for filename in translate_plain_text(po_filename, path, encoding, join_paragraphs):
        print(filename, file=sys.stderr)


if __name__ == "__main__":
    typer.run(main)
