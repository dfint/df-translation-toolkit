from collections.abc import Iterable
from pathlib import Path
from typing import TextIO

import typer

from df_translation_toolkit.utils import csv_utils
from df_translation_toolkit.utils.fix_translated_strings import cleanup_string, fix_spaces
from df_translation_toolkit.utils.po_utils import simple_read_po


def prepare_dictionary(dictionary: Iterable[tuple[str, str]]) -> Iterable[tuple[str, str]]:
    for original_string, translation in dictionary:
        if original_string and translation and translation != original_string:
            yield original_string, cleanup_string(fix_spaces(original_string, translation))


def convert(po_file: TextIO, csv_file: TextIO) -> None:
    dictionary = simple_read_po(po_file)
    csv_writer = csv_utils.writer(csv_file)

    for original_string, translation in prepare_dictionary(dictionary):
        csv_writer.writerow([original_string, translation])


app = typer.Typer()


@app.command()
def main(po_file: Path, csv_file: Path, encoding: str) -> None:
    """
    Convert a po file into a csv file in a specified encoding
    """

    with (
        po_file.open("r", encoding="utf-8") as pofile,
        csv_file.open("w", newline="", encoding=encoding, errors="replace") as outfile,
    ):
        convert(pofile, outfile)


if __name__ == "__main__":
    app()
