from pathlib import Path
from typing import Callable, Iterable, Iterator, NamedTuple, Sequence

import typer

from df_gettext_toolkit.translate_compressed import translate_compressed
from df_gettext_toolkit.translate_plain_text import translate_plain_text
from df_gettext_toolkit.translate_raws import translate_raws


class Pattern(NamedTuple):
    directory: str
    po_filename: str
    function: Callable[[Path, Path, str], Iterable[str]]


patterns = [
    Pattern("raw/objects", "raw-objects", translate_raws),
    Pattern("data", "uncompressed", translate_compressed),
    Pattern("data/speech", "speech", lambda *args: translate_plain_text(*args, join_paragraphs=False)),
    Pattern("raw/objects/text", "text", lambda *args: translate_plain_text(*args, join_paragraphs=False)),
]


def translate_files(
    base_path: Path,
    po_directory: Path,
    encoding: str,
    po_name_postfix: str = "",
    translate: bool = True,
    directory_patterns: Sequence[Pattern] = tuple(patterns),
) -> Iterator[str]:
    for cur_dir in base_path.rglob("*"):
        if cur_dir.is_dir():
            for directory, po_filename, function in directory_patterns:
                if cur_dir.match("*/" + directory):
                    yield f"Matched {directory} pattern"

                    po_filename = f"{po_filename}_{po_name_postfix}.po"
                    po_file_path = po_directory / po_filename

                    if translate:
                        for filename in function(po_file_path, cur_dir, encoding):
                            yield filename


def main(
    base_path: Path,
    po_directory: Path,
    encoding: str,
    po_name_postfix: str = "",
    translate: bool = True,
):
    for message in translate_files(base_path, po_directory, encoding, po_name_postfix, translate):
        print(message)


if __name__ == "__main__":
    typer.run(main)
