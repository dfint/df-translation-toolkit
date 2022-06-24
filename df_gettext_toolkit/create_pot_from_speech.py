import sys
from pathlib import Path
from typing import Iterator

import typer

from df_gettext_toolkit.common import TranslationItem
from df_gettext_toolkit.parse_po import save_pot


def convert_file_lines_to_translation_items(path: Path) -> Iterator[TranslationItem]:
    for file_path in sorted(path.glob("*.txt")):
        if file_path.is_file():
            print("File:", file_path.name, file=sys.stderr)
            with open(file_path) as file:
                for i, line in enumerate(file, 1):
                    text = line.rstrip("\n")
                    if text:
                        yield TranslationItem(text=text, source_file=file_path.name, line_number=i)


def main(
    path: Path,
    destination_file: typer.FileTextWrite = typer.Option(..., encoding="utf-8"),
):
    print("Path:", path, file=sys.stderr)
    save_pot(destination_file, convert_file_lines_to_translation_items(path))


if __name__ == "__main__":
    typer.run(main)
