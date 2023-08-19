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
from df_gettext_toolkit.utils.maybe_open import maybe_open


def all_caps(string: str):
    return len(string) > 1 and string.isupper()


def get_translations_from_tag_simple(original_parts: list[str], translation_parts: list[str]):
    tag_translations = defaultdict(list)

    prev_original = None
    prev_translation = None
    for original, translation in zip(original_parts, translation_parts):
        original: str
        if all_caps(original) or original.isdecimal():
            valid = original == translation or original in ("STP", "NP", "SINGULAR", "PLURAL")
            assert valid, f"Part {original!r} should not be translated"

            if original == "STP" and translation != original and not all_caps(translation):
                tag_translations[prev_original + "s"].append(translation)
                tag_translations[prev_translation + "s"].append(translation)
        elif original:
            assert translation, "Translation should not be empty"
            tag_translations[original].append(translation)
            prev_original = original
            prev_translation = translation

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


def get_translations_from_tag(original_tag: str, translation_tag: str):
    assert translation_tag.startswith("[") and translation_tag.endswith("]"), "Wrong tag translation format"
    assert all(char not in translation_tag[1:-1] for char in "[]"), "Wrong tag translation format"

    original_parts = split_tag(original_tag)
    translation_parts = split_tag(translation_tag)
    assert original_parts[0] == translation_parts[0], "First part of a tag should not be translated"
    assert len(original_parts) == len(translation_parts), "Tag parts count mismatch"
    original_parts = original_parts[1:]
    translation_parts = translation_parts[1:]

    yield from get_translations_from_tag_simple(original_parts, translation_parts)


def prepare_dictionary(dictionary: Iterable[tuple[str, str]], errors_file: TextIO) -> Iterable[tuple[str, str]]:
    for original_string_tag, translation_tag in dictionary:
        if original_string_tag and translation_tag and translation_tag != original_string_tag:
            try:
                for original_string, translation in get_translations_from_tag(original_string_tag, translation_tag):
                    translation = fix_spaces(original_string, translation)
                    yield original_string, cleanup_string(translation)
            except AssertionError as ex:
                error_text = f"Tag pair: {original_string_tag!r}, {translation_tag!r}\nError: {ex}"
                logger.error("\n" + error_text)
                if errors_file:
                    print(error_text, file=errors_file)


def convert(po_file: TextIO, csv_file: TextIO, error_file: TextIO = None):
    dictionary = [(item.id, item.string) for item in read_po(po_file) if item.id and item.string]
    csv_writer = csv_utils.writer(csv_file)
    for original_string, translation in dict(prepare_dictionary(dictionary, error_file)).items():
        csv_writer.writerow([original_string, translation])


app = typer.Typer()


@app.command()
def main(po_file: Path, csv_file: Path, encoding: str, append: bool = False, errors_file: Path = None):
    """
    Convert a po file into a csv file in a specified encoding
    """

    with open(po_file, "r", encoding="utf-8") as pofile:
        mode = "a" if append else "w"
        with open(csv_file, mode, newline="", encoding=encoding, errors="replace") as outfile:
            with maybe_open(errors_file, "w", encoding="utf-8") as errors_file:
                convert(pofile, outfile, errors_file)


if __name__ == "__main__":
    app()
