import sys

from pathlib import Path

import typer

from .backup import backup
from .parse_raws import translate_raw_file
from .po import load_po
from .fix_translated_strings import cleanup_string


def translate_raws(po_filename, path, encoding: str):
    with open(po_filename, 'r', encoding='utf-8') as pofile:
        dictionary = {(item['msgid'], item['msgctxt']): item['msgstr'] for item in load_po(pofile)}

    for file_path in Path(path).glob("*.txt"):
        if file_path.is_file() and not file_path.name.startswith('language_'):
            with backup(file_path) as bak_name:
                with open(bak_name, encoding='cp437') as src:
                    with open(file_path, 'w', encoding=encoding) as dest:
                        yield file_path.name
                        for line in translate_raw_file(src, dictionary):
                            line = cleanup_string(line)
                            try:
                                print(line, file=dest)
                            except UnicodeEncodeError:
                                line = line.encode(encoding, errors='backslashreplace').decode(encoding)
                                print('Some characters of this line: %r '
                                      'cannot be represented in %s encoding. Using backslashreplace mode.' %
                                      (line, encoding), file=sys.stderr)

                                print(line, file=dest)


def main(po_filename: str, path: str, encoding: str):
    for filename in translate_raws(po_filename, path, encoding):
        print(filename, file=sys.stderr)


if __name__ == "__main__":
    typer.run(main)
