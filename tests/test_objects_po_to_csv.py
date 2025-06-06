import pytest

from df_translation_toolkit.convert.objects_po_to_csv import get_translations_from_tag_parts


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
def test_get_translations_from_tag(
    original_parts: list[str],
    translation_parts: list[str],
    result: list[tuple[str, str]],
) -> None:
    assert list(get_translations_from_tag_parts(original_parts, translation_parts)) == result
