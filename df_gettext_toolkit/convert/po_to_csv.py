#! python3
from pathlib import Path
from typing import Iterable, Set, TextIO, Tuple

import typer
from babel.messages.pofile import read_po

from df_gettext_toolkit.utils import csv_utils
from df_gettext_toolkit.utils.fix_translated_strings import cleanup_string, fix_spaces


def prepare_dictionary(
    dictionary: Iterable[Tuple[str, str]],
    exclusions_leading: Set[str],
    exclusions_trailing: Set[str],
) -> Iterable[Tuple[str, str]]:
    for original_string, translation in dictionary:
        if original_string and translation and translation != original_string:
            translation = fix_spaces(original_string, translation, exclusions_leading, exclusions_trailing)
            yield original_string, cleanup_string(translation)


def convert(po_file: TextIO, csv_file: TextIO, encoding: str):
    dictionary = [(item.id, item.string) for item in read_po(po_file) if item.id and item.string]

    exclusions_leading = {"  Choose Name  ", "  Trade Agreement with "}
    exclusions_trailing = {"  Choose Name  "}

    if encoding == "cp1251":
        exclusions_trailing.add("Histories of ")

    csv_writer = csv_utils.writer(csv_file)

    for original_string, translation in prepare_dictionary(dictionary, exclusions_leading, exclusions_trailing):
        csv_writer.writerow([original_string, translation])


def main(po_file: Path, csv_file: Path, encoding: str):
    """
    Convert a po file into a csv file in a specified encoding
    """

    with po_file.open("r", encoding="utf-8") as pofile:
        with csv_file.open("w", newline="", encoding=encoding, errors="replace") as outfile:
            convert(pofile, outfile, encoding)


if __name__ == "__main__":
    typer.run(main)
