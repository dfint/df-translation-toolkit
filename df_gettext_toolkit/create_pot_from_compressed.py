import sys
from pathlib import Path
from typing import Sequence, Iterator, Iterable

import typer
from df_raw_decoder import unpack_data

from df_gettext_toolkit.common import TranslationItem
from df_gettext_toolkit.create_pot_from_plain_text import extract_translatables_from_file
from df_gettext_toolkit.parse_po import save_pot


def extract_translatables(files: Iterable[Path]) -> Iterator[TranslationItem]:
    keys = set()
    for file_path in files:
        print(file_path, file=sys.stderr)
        with open(file_path, "rb") as file:
            lines = unpack_data(file)
            yield from extract_translatables_from_file(lines, file_path, True, keys)


def create_pot_file(pot_file: typer.FileTextWrite, files: Sequence[Path]):
    save_pot(
        pot_file,
        extract_translatables(files),
    )


def main(path: Path, pot_file: typer.FileTextWrite):
    files = (file for file in path.glob("*") if file.is_file() and "." not in file.name and file.name != "index")
    create_pot_file(pot_file, sorted(files))


if __name__ == "__main__":
    typer.run(main)
