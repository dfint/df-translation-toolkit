from collections import defaultdict
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import TextIO

import typer
from loguru import logger

from df_translation_toolkit.parse.parse_raws import all_caps, split_tag
from df_translation_toolkit.utils import csv_utils
from df_translation_toolkit.utils.fix_translated_strings import cleanup_string, fix_spaces
from df_translation_toolkit.utils.maybe_open import maybe_open
from df_translation_toolkit.utils.po_utils import simple_read_po
from df_translation_toolkit.validation.validate_objects import validate_tag
from df_translation_toolkit.validation.validation_models import ValidationException, ValidationProblem


def get_translations_from_tag_parts(
    original_parts: list[str],
    translation_parts: list[str],
) -> Iterator[tuple[str, str]]:
    tag_translations = defaultdict(list)

    prev_original = None
    prev_translation = None
    for original, translation in zip(original_parts, translation_parts, strict=False):
        original: str
        if all_caps(original) or original.isdecimal():
            if original == "STP" and translation != original and not all_caps(translation):
                tag_translations[prev_original + "s"].append(translation)
                tag_translations[prev_translation + "s"].append(translation)
        elif original:
            tag_translations[original].append(translation)
            prev_original = original
            prev_translation = translation

    for original, translations in tag_translations.items():
        yield original, translations[0]


def get_translations_from_tag(original_tag: str, translation_tag: str) -> Iterator[tuple[str, str]]:
    validation_problems = list(validate_tag(original_tag, translation_tag))
    if ValidationProblem.contains_errors(validation_problems):
        raise ValidationException(validation_problems)

    original_parts = split_tag(original_tag)
    translation_parts = split_tag(translation_tag)
    original_parts = original_parts[1:]
    translation_parts = translation_parts[1:]

    yield from get_translations_from_tag_parts(original_parts, translation_parts)
    if validation_problems:
        raise ValidationException(validation_problems)  # pass warnings


def prepare_dictionary(dictionary: Iterable[tuple[str, str]], errors_file: TextIO) -> Iterable[tuple[str, str]]:
    for original_string_tag, translation_tag in dictionary:
        if original_string_tag and translation_tag and translation_tag != original_string_tag:
            try:
                for original_string, translation in get_translations_from_tag(original_string_tag, translation_tag):
                    yield original_string, cleanup_string(fix_spaces(original_string, translation))
            except ValidationException as ex:
                error_text = f"Problematic tag pair: {original_string_tag!r}, {translation_tag!r}\nProblems:\n{ex}"
                logger.error("\n" + error_text)
                if errors_file:
                    print(error_text, end="\n\n", file=errors_file)


def convert(po_file: TextIO, csv_file: TextIO, error_file: TextIO | None = None) -> None:
    dictionary = simple_read_po(po_file)
    csv_writer = csv_utils.writer(csv_file)

    for original_string, translation in dict(prepare_dictionary(dictionary, error_file)).items():
        csv_writer.writerow([original_string, translation])


app = typer.Typer()


@app.command()
def main(
    po_file: Path,
    csv_file: Path,
    encoding: str,
    append: bool = False,  # noqa: FBT001, FBT002
    errors_file_path: Path | None = None,
) -> None:
    """
    Convert a po file into a csv file in a specified encoding
    """

    with open(po_file, encoding="utf-8") as pofile:
        mode = "a" if append else "w"
        with (
            open(csv_file, mode, newline="", encoding=encoding, errors="replace") as outfile,
            maybe_open(errors_file_path, "w", encoding="utf-8") as errors_file,
        ):
            convert(pofile, outfile, errors_file)


if __name__ == "__main__":
    app()
