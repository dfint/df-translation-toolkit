from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import TextIO

import typer
from babel.messages.pofile import read_po
from loguru import logger

from df_gettext_toolkit.parse.parse_raws import split_tag
from df_gettext_toolkit.utils import csv_utils
from df_gettext_toolkit.utils.fix_translated_strings import cleanup_string, fix_spaces


def all_caps(string: str):
    return len(string) > 1 and string.isupper()


def get_translations_from_tag_simple(original_parts: list[str], translation_parts: list[str]):
    tag_translations = defaultdict(list)

    for original, translation in zip(original_parts, translation_parts):
        if all_caps(original):
            # don't translate caps parts like NP, SINGULAR, PLURAL, etc.
            # (except for STP, but it is handled separately)
            pass
        elif original:
            assert translation, "Translation should not be empty"
            tag_translations[original].append(translation)

    for original, translations in tag_translations.items():
        yield original, translations[0]


def get_translations_from_tag_stp(original_parts: list[str], translation_parts: list[str]):
    """
    Handle STP (standard plural) case
    """
    original = original_parts[0]
    singular_translation = translation_parts[0]

    yield original, singular_translation

    plural_translation = translation_parts[1]
    if plural_translation in ("STP", "NP"):
        return

    yield original + "s", plural_translation
    yield singular_translation + "s", plural_translation


@logger.catch
def get_translations_from_tag(original_tag: str, translation_tag: str):
    assert translation_tag.startswith("[") and translation_tag.endswith("]"), "Wrong tag translation format"
    assert all(char not in translation_tag[1:-1] for char in "[]"), "Wrong tag translation format"

    original_parts = split_tag(original_tag)
    translation_parts = split_tag(translation_tag)
    assert original_parts[0] == translation_parts[0], "First part of a tag should not be translated"
    assert len(original_parts) == len(translation_tag), "Tag parts count mismatch"
    original_parts = original_parts[1:]
    translation_parts = translation_parts[1:]

    if len(original_parts) == 2 and original_parts[1] == "STP":
        yield from get_translations_from_tag_stp(original_parts, translation_parts)
    else:
        yield from get_translations_from_tag_simple(original_parts, translation_parts)


def prepare_dictionary(dictionary: Iterable[tuple[str, str]]) -> Iterable[tuple[str, str]]:
    for original_string_tag, translation_tag in dictionary:
        if original_string_tag and translation_tag and translation_tag != original_string_tag:
            for original_string, translation in get_translations_from_tag(original_string_tag, translation_tag):
                translation = fix_spaces(original_string, translation)
                yield original_string, cleanup_string(translation)


def convert(po_file: TextIO, csv_file: TextIO):
    dictionary = [(item.id, item.string) for item in read_po(po_file) if item.id and item.string]
    csv_writer = csv_utils.writer(csv_file)
    for original_string, translation in prepare_dictionary(dictionary):
        csv_writer.writerow([original_string, translation])


app = typer.Typer()


@app.command()
def main(po_file: Path, csv_file: Path, encoding: str, append: bool = False):
    """
    Convert a po file into a csv file in a specified encoding
    """

    with open(po_file, "r", encoding="utf-8") as pofile:
        mode = "a" if append else "w"
        with open(csv_file, mode, newline="", encoding=encoding, errors="replace") as outfile:
            convert(pofile, outfile)


if __name__ == "__main__":
    app()
