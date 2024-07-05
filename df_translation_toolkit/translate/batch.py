from collections.abc import Callable, Iterable, Iterator, Sequence
from pathlib import Path
from typing import NamedTuple

import typer

from df_translation_toolkit.translate.translate_plain_text import translate_plain_text
from df_translation_toolkit.translate.translate_raws import translate_raws


class Pattern(NamedTuple):
    directory: str
    po_filename: str
    function: Callable[[Path, Path, str], Iterable[str]]


patterns = [
    Pattern("raw/objects", "raw-objects", translate_raws),
    Pattern("data/speech", "speech", lambda *args: translate_plain_text(*args, join_paragraphs=False)),
    Pattern("raw/objects/text", "text", lambda *args: translate_plain_text(*args, join_paragraphs=False)),
]


def translate_files(  # noqa: PLR0913
    base_path: Path,
    po_directory: Path,
    encoding: str,
    po_name_postfix: str = "",
    *,
    translate: bool = True,
    directory_patterns: Sequence[Pattern] = tuple(patterns),
) -> Iterator[str]:
    for cur_dir in base_path.rglob("*"):
        if cur_dir.is_dir():
            for directory, po_filename, function in directory_patterns:
                if cur_dir.match("*/" + directory):
                    yield f"Matched {directory} pattern"

                    filename = f"{po_filename}_{po_name_postfix}.po"
                    po_file_path = po_directory / filename

                    if translate:
                        yield from function(po_file_path, cur_dir, encoding)


def main(
    base_path: Path,
    po_directory: Path,
    encoding: str,
    po_name_postfix: str = "",
    translate: bool = True,  # noqa: FBT001, FBT002
) -> None:
    for message in translate_files(base_path, po_directory, encoding, po_name_postfix, translate):
        print(message)


if __name__ == "__main__":
    typer.run(main)
