import os
import sys

import typer

from .parse_raws import extract_translatables_from_raws
from .po import format_po, default_pot_header


def main(pot_filename, path: str = '.', source_encoding: str = 'cp437'):
    raw_files = filter(lambda x: not x.startswith('language_'), os.listdir(path))

    with open(pot_filename, 'w', encoding='utf-8') as pot_file:
        print(default_pot_header, file=pot_file)
        for file_name in sorted(raw_files):
            full_path = os.path.join(path, file_name)
            if os.path.isfile(full_path) and file_name.endswith('.txt'):
                print(file_name, file=sys.stderr)
                with open(full_path, encoding=source_encoding) as file:
                    for context, item, line_number in extract_translatables_from_raws(file):
                        print('#: %s:%d' % (file_name, line_number), file=pot_file)  # source file : line number
                        print(format_po(msgid=item, msgstr="", msgctxt=context), file=pot_file)


if __name__ == '__main__':
    typer.run(main)
