import sys
from pathlib import Path
from typing import Iterable, Iterator, Sequence, TextIO

import typer

from df_gettext_toolkit.utils.po_utils import TranslationItem, save_pot


def extract_from_speech_file(file: TextIO, source_path: str):
    for i, line in enumerate(file, 1):
        text = line.rstrip("\n")
        if text:
            yield TranslationItem(text=text, source_file=source_path, line_number=i)


def extract_translatables(files: Iterable[Path]) -> Iterator[TranslationItem]:
    for file_path in files:
        if file_path.is_file():
            print("File:", file_path.name, file=sys.stderr)
            with file_path.open() as file:
                yield from extract_from_speech_file(file, file_path.name)


def create_pot_file(pot_file: typer.FileBinaryWrite, files: Sequence[Path]):
    save_pot(
        pot_file,
        extract_translatables(files),
    )


def main(
    path: Path,
    pot_file: typer.FileBinaryWrite,
):
    files = (file for file in path.glob("*.txt") if file.is_file())
    create_pot_file(pot_file, sorted(files))


if __name__ == "__main__":
    typer.run(main)
