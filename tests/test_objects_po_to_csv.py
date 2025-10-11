import pytest

from df_translation_toolkit.convert.objects_po_to_csv import (
    get_translations_from_tag,
    get_translations_from_tag_parts,
    validate_string,
)


@pytest.mark.parametrize(
    "original_parts,translation_parts,result",
    [
        (
            # TODO(@insolor): replace this test with a hypothesis test
            ["abc", "cde", "def"],
            ["wefw", "rtt", "jty"],
            [("abc", "wefw"), ("cde", "rtt"), ("def", "jty")],
        ),
        (
            ["abc", "NP"],
            ["def", "defs"],
            [("abc", "def")],
        ),
        (
            ["cake", "STP"],
            ["торт", "торты"],
            [("cake", "торт"), ("cakes", "торты"), ("тортs", "торты")],
        ),
    ],
)
def test_get_translations_from_tag_parts(
    original_parts: list[str],
    translation_parts: list[str],
    result: list[tuple[str, str]],
) -> None:
    assert list(get_translations_from_tag_parts(original_parts, translation_parts)) == result


@pytest.mark.parametrize(
    "original_tag,translation_tag,result",
    [
        (
            "[INDIVIDUAL_NAME:first upper left premolar:STP]",
            "[INDIVIDUAL_NAME:верхний левый первый премоляр:верхние левые первые премоляры]",
            [
                ("first upper left premolar", "верхний левый первый премоляр"),
                ("first upper left premolars", "верхние левые первые премоляры"),
                ("верхний левый первый премолярs", "верхние левые первые премоляры"),
            ],
        ),
    ],
)
def test_get_translation_from_tag(
    original_tag: str,
    translation_tag: str,
    result: list[tuple[str, str]],
) -> None:
    assert list(get_translations_from_tag(original_tag, translation_tag)) == result


@pytest.mark.parametrize(
    "original_tag,translation_tag,result",
    [
        (
            "[INDIVIDUAL_NAME:first upper left premolar:STP]",
            "[INDIVIDUAL_NAME:верхний левый первый премоляр:верхние левые первые премоляры]",
            [
                ("first upper left premolar", "верхний левый первый премоляр"),
                ("first upper left premolars", "верхние левые первые премоляры"),
                ("верхний левый первый премолярs", "верхние левые первые премоляры"),
            ],
        ),
        ("[PREFSTRING:something]", "    [PREFSTRING:translation]    ", [("something", "translation")]),
    ],
)
def test_validate_string(
    original_tag: str,
    translation_tag: str,
    result: list[tuple[str, str]],
) -> None:
    validation_result = validate_string(original_tag, translation_tag)
    assert validation_result is not None
    assert list(validation_result) == result
