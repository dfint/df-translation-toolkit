from collections.abc import Iterable
from typing import BinaryIO, TextIO

from babel.messages.catalog import Catalog, Message
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
from loguru import logger

from df_translation_toolkit.utils.fix_translated_strings import cleanup_string, fix_spaces
from df_translation_toolkit.validation.validate_general import validate
from df_translation_toolkit.validation.validation_models import Diagnostics, ProblemInfo


def validate_translation(
    original: str,
    translation: str,
    diagnostics: Diagnostics | None = None,
) -> str | None:
    validation_problems = list(validate(original, translation))
    if validation_problems:
        problem_info = ProblemInfo(original=original, translation=translation, problems=validation_problems)
        logger.error("\n" + str(problem_info))
        if diagnostics:
            diagnostics.add(problem_info)

        if problem_info.contains_errors():
            return None

    return fix_spaces(original, translation)


def translate_tag_string(
    original: str,
    translation: str,
    diagnostics: Diagnostics | None = None,
) -> str | None:
    if not (original and translation and translation != original):
        return None

    validated_translation = validate_translation(original, translation, diagnostics=diagnostics)
    if not validated_translation:
        return None

    return cleanup_string(validated_translation)


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
