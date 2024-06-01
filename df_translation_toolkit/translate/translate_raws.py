import sys
from collections.abc import Iterator, Mapping
from pathlib import Path

import typer
from babel.messages.pofile import read_po

from df_translation_toolkit.parse.parse_raws import translate_raw_file
from df_translation_toolkit.utils.backup import backup
from df_translation_toolkit.utils.fix_translated_strings import cleanup_string


def translate_single_raw_file(
    source_file_path: Path,
    destination_file_path: Path,
    dictionary: Mapping[tuple[str, str | None], str],
    encoding: str,
) -> Iterator[str]:
    with source_file_path.open(encoding="cp437") as src, destination_file_path.open("w", encoding=encoding) as dest:
        yield destination_file_path.name
        for line in translate_raw_file(src, dictionary):
            line = cleanup_string(line)
            try:
                print(line, file=dest)
            except UnicodeEncodeError:
                line = line.encode(encoding, errors="backslashreplace").decode(encoding)
                print(
                    f"Some characters of this line: {line!r} "
                    f"cannot be represented in {encoding} encoding. Using backslashreplace mode.",
                    file=sys.stderr,
                )

                print(line, file=dest)


def translate_raws(po_filename: Path, path: Path, encoding: str) -> Iterator[str]:
    with po_filename.open("r", encoding="utf-8") as pofile:
        dictionary = {(item.id, item.context): item.string for item in read_po(pofile)}

    for file_path in path.glob("*.txt"):
        if file_path.is_file() and not file_path.name.startswith("language_"):
            with backup(file_path) as bak_name:
                yield from translate_single_raw_file(bak_name, file_path, dictionary, encoding)


def main(po_filename: Path, path: Path, encoding: str) -> str:
    for filename in translate_raws(po_filename, path, encoding):
        print(filename, file=sys.stderr)


if __name__ == "__main__":
    typer.run(main)
