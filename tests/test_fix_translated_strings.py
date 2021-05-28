import pytest

from df_gettext_toolkit.fix_translated_strings import cleanup_string
from df_gettext_toolkit.fix_translated_strings import fix_leading_spaces, fix_trailing_spaces, fix_spaces


@pytest.mark.parametrize(
    "original,fixed",
    [
        ('kožušček', 'kožušček'),  # must not remove diacritics
        ('\ufeff\u200b', ''),  # remove zero width characters
        ('—', '-'),  # use standard dash instead of Em Dash
        (""" ‘’”“ """, """ ''"" """),  # Fix quotes
        ('¿Qué dirás?', '¿Qué dirás?'),  # Don't change Spanish question mark
        ('¡Hace un frio helador!', '¡Hace un frio helador!'),  # Don't change Spanish exclamation mark
    ]
)
def test_cleanup_string(original, fixed):
    assert cleanup_string(original) == fixed


@pytest.mark.parametrize(
    "text,translation,fixed",
    [
        (" test", "test", " test"),
        ("test", " test", "test"),
        (" test", ", test", ", test"),
        (".  What do you command?", " . ¿Qué ordenas?", ". ¿Qué ordenas?"),
    ]
)
def test_fix_leading_spaces(text, translation, fixed):
    assert fix_leading_spaces(text, translation, set()) == fixed


@pytest.mark.parametrize(
    "text,translation,fixed",
    [
        ("test ", "test", "test "),
        # ("test", "test ", "test"),
    ]
)
def test_fix_trailing_spaces(text, translation, fixed):
    assert fix_trailing_spaces(text, translation, set()) == fixed


@pytest.mark.parametrize(
    "text,translation,fixed",
    [
        (" embraces ", "obdivuje", " obdivuje "),
    ]
)
def test_fix_spaces(text, translation, fixed):
    assert fix_spaces(text, translation) == fixed
