import pytest

from df_gettext_toolkit.convert.objects_po_to_csv import get_translations_from_tag_simple, get_translations_from_tag_stp


@pytest.mark.parametrize(
    "original_parts,translation_parts,result",
    [
        (
            # TODO: replace this test with a hypothesis test
            ["abc", "cde", "def"],
            ["wefw", "rtt", "jty"],
            [("abc", "wefw"), ("cde", "rtt"), ("def", "jty")],
        ),
        (
            ["abc", "NP"],
            ["def", "defs"],
            [("abc", "def")],
        ),
    ],
)
def test_get_translations_from_tag_simple(original_parts, translation_parts, result):
    assert list(get_translations_from_tag_simple(original_parts, translation_parts)) == result


@pytest.mark.parametrize(
    "original_parts,translation_parts,result",
    [
        (
            ["cake", "STP"],
            ["торт", "торты"],
            [("cake", "торт"), ("cakes", "торты"), ("тортs", "торты")],
        ),
    ],
)
def test_get_translations_from_tag_stp(original_parts, translation_parts, result):
    assert list(get_translations_from_tag_stp(original_parts, translation_parts)) == result
