import pytest

from df_translation_toolkit.convert.objects_po_to_mo import fix_spaces_in_tag_parts_translations, translate_tag_string


@pytest.mark.parametrize(
    "original_parts, translated_parts, result",
    [
        (["FIRST", " original "], ["FIRST", "translation"], ["FIRST", " translation "]),
    ],
)
def test_fix_spaces_in_tag_parts_translations(
    original_parts: list[str],
    translated_parts: list[str],
    result: list[str],
) -> None:
    assert list(fix_spaces_in_tag_parts_translations(original_parts, translated_parts)) == result


@pytest.mark.parametrize(
    "original, translation, result",
    [
        ("[FIRST: original ]", "[FIRST:translation]", "[FIRST: translation ]"),
        ("[FIRST:original]", "[FIRST: translation ]", "[FIRST:translation]"),
        ("[FIRST:original]", " [FIRST:translation] ", "[FIRST:translation]"),
    ],
)
def test_translate_tag_string(original: str, translation: str, result: str) -> None:
    assert translate_tag_string(original, translation) == result
