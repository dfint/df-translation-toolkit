import pytest

from df_gettext_toolkit.convert.objects_po_to_csv import get_translations_from_tag_simple


@pytest.mark.parametrize(
    "original_parts,translation_parts,result",
    [
        (
            # TODO: replace this test with a hypothesis test
            ["abc", "cde", "def"],
            ["wefw", "rtt", "jty"],
            [("abc", "wefw"), ("cde", "rtt"), ("def", "jty")],
        ),
    ],
)
def test_get_translations_from_tag_simple(original_parts, translation_parts, result):
    assert list(get_translations_from_tag_simple(original_parts, translation_parts)) == result
