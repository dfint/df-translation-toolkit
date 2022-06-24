import sys
from pathlib import Path
from typing import Iterator

import typer

from df_gettext_toolkit.common import TranslationItem
from df_gettext_toolkit.parse_plain_text import parse_plain_text_file
from df_gettext_toolkit.parse_po import save_pot


def convert_file_lines_to_translation_items(path: Path, join_paragraphs: bool) -> Iterator[TranslationItem]:
    keys = set()
    for file_path in sorted(path.rglob("*.txt")):
        if file_path.is_file():
            print(file_path, file=sys.stderr)
            with open(file_path) as file:
                for text_block, is_translatable, line_number in parse_plain_text_file(file, join_paragraphs):
                    if is_translatable:
                        if text_block in keys:
                            print("Key already exists:", repr(text_block), file=sys.stderr)
                        else:
                            keys.add(text_block)
                            yield TranslationItem(
                                text=text_block.rstrip("\n"), source_file=file_path.name, line_number=line_number
                            )


def main(path: Path, destination_file: typer.FileTextWrite = typer.Option(..., encoding="utf-8"), split: bool = False):
    save_pot(destination_file, convert_file_lines_to_translation_items(path, not split))


if __name__ == "__main__":
    typer.run(main)
