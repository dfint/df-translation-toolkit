import io
import sys
from pathlib import Path
from typing import Iterator

import typer

from .parse_po import format_po_item, default_header
from .parse_raws import extract_translatables_from_raws


def create_pot_file(pot_file: io.TextIOWrapper, raw_files: Iterator[Path], source_encoding: str):
    print(default_header, file=pot_file)
    for file_name in raw_files:
        if file_name.is_file():
            print(file_name.name, file=sys.stderr)
            with open(file_name, encoding=source_encoding) as file:
                for context, item, line_number in extract_translatables_from_raws(file):
                    print(
                        format_po_item(msgid=item, msgctxt=context, file_name=file_name.name, line_number=line_number),
                        end="\n\n",
                        file=pot_file,
                    )


def main(pot_file: typer.FileTextWrite, raws_path: Path, source_encoding: str = "cp437"):
    raw_files = (file for file in raws_path.glob("*.txt") if not file.name.startswith("language_"))
    create_pot_file(pot_file, sorted(raw_files), source_encoding)


if __name__ == "__main__":
    typer.run(main)
