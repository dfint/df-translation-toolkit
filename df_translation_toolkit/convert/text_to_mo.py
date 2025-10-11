from collections.abc import Iterable, Iterator
from typing import BinaryIO, TextIO

from babel.messages.catalog import Catalog, Message
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
from loguru import logger

from df_translation_toolkit.parse.parse_raws import join_tag, split_tag
from df_translation_toolkit.utils.fix_translated_strings import cleanup_string, fix_spaces
from df_translation_toolkit.validation.validate_objects import validate_tag
from df_translation_toolkit.validation.validation_models import Diagnostics, ProblemInfo


def fix_spaces_in_tag_parts_translations(original_parts: list[str], translation_parts: list[str]) -> Iterator[str]:
    for original, translation in zip(original_parts, translation_parts, strict=False):
        yield fix_spaces(original, translation, strict=True)


def translate_tag(
    original_tag: str,
    translation_tag: str,
    diagnostics: Diagnostics | None = None,
) -> str | None:
    validation_problems = list(validate_tag(original_tag, translation_tag))
    if validation_problems:
        problem_info = ProblemInfo(original=original_tag, translation=translation_tag, problems=validation_problems)
        logger.error("\n" + str(problem_info))
        if diagnostics:
            diagnostics.add(problem_info)

        if problem_info.contains_errors():
            return None

    translation_tag = fix_spaces(original_tag, translation_tag, strict=True)
    original_parts = split_tag(original_tag)
    translation_parts = split_tag(translation_tag)

    return join_tag(fix_spaces_in_tag_parts_translations(original_parts, translation_parts))


def translate_tag_string(
    original_string_tag: str,
    translation_tag: str,
    diagnostics: Diagnostics | None = None,
) -> str | None:
    if not (original_string_tag and translation_tag and translation_tag != original_string_tag):
        return None

    translation = translate_tag(original_string_tag, translation_tag, diagnostics=diagnostics)
    if not translation:
        return None

    return cleanup_string(translation)


def prepare_translation_messages(catalog: Catalog, diagnostics: Diagnostics | None = None) -> Iterable[Message]:
    for message in catalog:
        translation = translate_tag_string(str(message.id), str(message.string), diagnostics=diagnostics)
        if translation:
            yield Message(id=message.id, context=message.context, string=translation)


def convert(po_file: TextIO, mo_file: BinaryIO, diagnostics: Diagnostics | None = None) -> None:
    input_catalog = read_po(po_file)
    output_catalog = Catalog()

    for message in prepare_translation_messages(input_catalog, diagnostics):
        output_catalog.add(id=message.id, context=message.context, string=message.string)

    write_mo(mo_file, output_catalog)
