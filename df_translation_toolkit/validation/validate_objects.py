from collections.abc import Iterator

from df_translation_toolkit.parse.parse_raws import all_caps, split_tag
from df_translation_toolkit.validation.validation_models import ProblemSeverity, ValidationProblem


def validate_brackets(tag: str) -> bool:
    return tag.startswith("[") and tag.endswith("]") and tag.count("[") == 1 and tag.count("]") == 1


def validate_tag(original_tag: str, translation_tag: str) -> Iterator[ValidationProblem]:
    if len(translation_tag) <= 2:
        yield ValidationProblem("Too short or empty translation")
        return

    if not translation_tag.strip() == translation_tag:
        yield ValidationProblem("Extra spaces at the beginning or at the end of the translation")
        translation_tag = translation_tag.strip()
        # No return to check issues with brackets after stripping spaces

    if not validate_brackets(translation_tag):
        yield ValidationProblem("Wrong tag translation format (fix square brackets)")
        return

    original_parts = split_tag(original_tag)
    translation_parts = split_tag(translation_tag)

    if len(original_parts) != len(translation_parts):
        yield ValidationProblem("Tag parts count mismatch")
        return

    yield from validate_tag_parts(original_parts, translation_parts)


def validate_tag_parts(original_parts: list[str], translation_parts: list[str]) -> Iterator[ValidationProblem]:
    for original, translation in zip(original_parts, translation_parts):
        if all_caps(original) or original.isdecimal():
            valid = not (original != translation and original == translation.strip())
            if not valid:
                yield ValidationProblem("Don't add extra spaces at the beginning or at the end of a tag part")

            valid = original == translation or original in ("STP", "NP", "SINGULAR", "PLURAL")
            if not valid:
                yield ValidationProblem(f"Part {original!r} should not be translated")

            valid = original not in {"SINGULAR", "PLURAL"} or translation in {"SINGULAR", "PLURAL"}
            if not valid:
                yield ValidationProblem(
                    "SINGULAR can be changed only to PLURAL, and PLURAL can be changed only to SINGULAR"
                )

            if original == "STP" and translation == "STP":
                yield ValidationProblem(
                    "Replace STP with a translation of the previous word in the tag in a plural form, "
                    "otherwise, the game will create a plural form with adding -s at the end. "
                    "If the translation with adding -s at the end is valid for your language, "
                    "just ignore this message.",
                    ProblemSeverity.WARNING,
                )
        elif original and not translation:
            yield ValidationProblem("Translation should not be empty")
