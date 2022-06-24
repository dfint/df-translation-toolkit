import sys
from pathlib import Path
from typing import Mapping, Optional, Tuple

import typer

from df_gettext_toolkit.backup import backup
from df_gettext_toolkit.fix_translated_strings import cleanup_string
from df_gettext_toolkit.parse_po import load_po
from df_gettext_toolkit.parse_raws import translate_raw_file


def translate_single_raw_file(
    source_file_path: Path,
    destination_file_path: Path,
    dictionary: Mapping[Tuple[str, Optional[str]], str],
    encoding: str,
):

    with open(source_file_path, encoding="cp437") as src:
        with open(destination_file_path, "w", encoding=encoding) as dest:
            yield destination_file_path.name
            for line in translate_raw_file(src, dictionary):
                line = cleanup_string(line)
                try:
                    print(line, file=dest)
                except UnicodeEncodeError:
                    line = line.encode(encoding, errors="backslashreplace").decode(encoding)
                    print(
                        "Some characters of this line: %r "
                        "cannot be represented in %s encoding. Using backslashreplace mode." % (line, encoding),
                        file=sys.stderr,
                    )

                    print(line, file=dest)


def translate_raws(po_filename, path, encoding: str):
    with open(po_filename, "r", encoding="utf-8") as pofile:
        dictionary = {(item.text, item.context): item.translation for item in load_po(pofile)}

    for file_path in Path(path).glob("*.txt"):
        if file_path.is_file() and not file_path.name.startswith("language_"):
            with backup(file_path) as bak_name:
                yield from translate_single_raw_file(bak_name, file_path, dictionary, encoding)


def main(po_filename: str, path: str, encoding: str):
    for filename in translate_raws(po_filename, path, encoding):
        print(filename, file=sys.stderr)


if __name__ == "__main__":
    typer.run(main)
