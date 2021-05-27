import pytest

from df_gettext_toolkit.fix_translated_strings import cleanup_string


@pytest.mark.parametrize(
    "original,fixed",
    [
        ('kožušček', 'kožušček'),  # must not remove diacritics
        ('\ufeff\u200b', ''),  # remove zero width characters
        ('—', '-'),  # use standard dash instead of Em Dash
        (""" ‘’”“ """, """ ''"" """),  # Fix quotes
    ]
)
def test_cleanup_string(original, fixed):
    assert cleanup_string(original) == fixed
