from collections import defaultdict
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import IO, TextIO

import typer
from loguru import logger

from df_translation_toolkit.parse.parse_raws import all_caps, split_tag
from df_translation_toolkit.utils import csv_utils
from df_translation_toolkit.utils.fix_translated_strings import cleanup_string, fix_spaces
from df_translation_toolkit.utils.po_utils import simple_read_po
from df_translation_toolkit.validation.validate_objects import validate_tag
from df_translation_toolkit.validation.validation_models import (
    Diagnostics,
    ProblemInfo,
    ValidationException,
    ValidationProblem,
)


def get_translations_from_tag_parts(
    original_parts: list[str],
    translation_parts: list[str],
) -> Iterator[tuple[str, str]]:
    tag_translations = defaultdict(list)

    prev_original = ""
    prev_translation = ""
    for original, translation in zip(original_parts, translation_parts, strict=False):
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

    translation_tag = fix_spaces(original_tag, translation_tag, strict=True)
    original_parts = split_tag(original_tag)
    translation_parts = split_tag(translation_tag)
    original_parts = original_parts[1:]
    translation_parts = translation_parts[1:]

    yield from get_translations_from_tag_parts(original_parts, translation_parts)
    if validation_problems:
        raise ValidationException(validation_problems)  # pass warnings


def validate_string(
    original_string_tag: str,
    translation_tag: str,
    diagnostics: Diagnostics | None = None,
) -> Iterable[tuple[str, str]]:
    if not (original_string_tag and translation_tag and translation_tag != original_string_tag):
        return None

    try:
        for original_string, translation in get_translations_from_tag(original_string_tag, translation_tag):
            yield original_string, cleanup_string(fix_spaces(original_string, translation))
    except ValidationException as ex:
        problem_info = ProblemInfo(original=original_string_tag, translation=translation_tag, problems=ex.problems)
        logger.error("\n" + str(problem_info))
        if diagnostics:
            diagnostics.add(problem_info)


def prepare_dictionary(
    dictionary: Iterable[tuple[str, str]],
    diagnostics: Diagnostics | None = None,
) -> Iterable[tuple[str, str]]:
    for original_string_tag, translation_tag in dictionary:
        yield from validate_string(original_string_tag, translation_tag, diagnostics=diagnostics)


def convert(po_file: TextIO, csv_file: IO[str], diagnostics: Diagnostics | None = None) -> None:
    dictionary = simple_read_po(po_file)
    csv_writer = csv_utils.writer(csv_file)

    for original_string, translation in dict(prepare_dictionary(dictionary, diagnostics)).items():
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
        diagnostics = Diagnostics()
        with open(csv_file, mode, newline="", encoding=encoding, errors="replace") as outfile:
            convert(pofile, outfile, diagnostics)

        if errors_file_path and diagnostics:
            with open(errors_file_path, mode, encoding="utf-8") as errors_file:
                errors_file.write(str(diagnostics))


if __name__ == "__main__":
    app()
