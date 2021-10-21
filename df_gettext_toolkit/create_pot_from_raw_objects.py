import sys
from pathlib import Path
from typing import Iterator

import typer

from .parse_po import format_po, default_header
from .parse_raws import extract_translatables_from_raws


def create_pot_file(pot_file, raw_files: Iterator[Path], source_encoding):
    print(default_header, file=pot_file)
    for file_name in raw_files:
        if file_name.is_file():
            print(file_name.name, file=sys.stderr)
            with open(file_name, encoding=source_encoding) as file:
                for context, item, line_number in extract_translatables_from_raws(file):
                    print('#: %s:%d' % (file_name.name, line_number), file=pot_file)  # source file : line number
                    print(format_po(msgid=item, msgstr="", msgctxt=context), file=pot_file)


def main(pot_filename, path: str = '.', source_encoding: str = 'cp437'):
    raw_files = (file for file in Path(path).glob("*.txt") if not file.name.startswith("language_"))

    with open(pot_filename, 'w', encoding='utf-8') as pot_file:
        create_pot_file(pot_file, sorted(raw_files), source_encoding)


if __name__ == '__main__':
    typer.run(main)
