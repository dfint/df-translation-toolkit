#! python3
from typing import Iterable, Set, Tuple

import typer

from df_gettext_toolkit.parse.parse_po import load_po
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


def main(po_file: str, csv_file: str, encoding: str):
    """
    Convert a po file into a csv file in a specified encoding
    """

    with open(po_file, "r", encoding="utf-8") as pofile:
        dictionary = [(item.text, item.translation) for item in load_po(pofile) if item.text]

    exclusions_leading = {"  Choose Name  ", "  Trade Agreement with "}
    exclusions_trailing = {"  Choose Name  "}

    if encoding == "cp1251":
        exclusions_trailing.add("Histories of ")

    with open(csv_file, "w", newline="", encoding=encoding, errors="replace") as outfile:
        csv_writer = csv_utils.writer(outfile)

        for original_string, translation in prepare_dictionary(dictionary, exclusions_leading, exclusions_trailing):
            csv_writer.writerow([original_string, translation])


if __name__ == "__main__":
    typer.run(main)
