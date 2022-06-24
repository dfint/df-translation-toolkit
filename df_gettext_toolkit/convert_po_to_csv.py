#! python3
import csv
from typing import Iterable, Set, Tuple

import typer

from .fix_translated_strings import cleanup_string, fix_spaces
from .parse_po import escape_string, load_po


def prepare_dictionary(
    dictionary: Iterable[Tuple[str, str]],
    exclusions_leading: Set[str],
    exclusions_trailing: Set[str],
) -> Iterable[Tuple[str, str]]:

    for original_string, translation in dictionary:
        if original_string and translation and translation != original_string:
            translation = fix_spaces(original_string, translation, exclusions_leading, exclusions_trailing)
            yield original_string, cleanup_string(translation)


def main(input_file: str, output_file: str, encoding: str = "utf-8"):
    with open(input_file, "r", encoding="utf-8") as pofile:
        dictionary = [(item["msgid"], item["msgstr"]) for item in load_po(pofile) if item["msgid"]]

    exclusions_leading = {"  Choose Name  ", "  Trade Agreement with "}
    exclusions_trailing = {"  Choose Name  "}

    if encoding == "cp1251":
        exclusions_trailing.add("Histories of ")

    with open(output_file, "w", newline="", encoding=encoding, errors="replace") as outfile:
        writer = csv.writer(outfile, dialect="unix")

        for original_string, translation in prepare_dictionary(dictionary, exclusions_leading, exclusions_trailing):
            writer.writerow([escape_string(original_string), escape_string(translation)])


if __name__ == "__main__":
    typer.run(main)
