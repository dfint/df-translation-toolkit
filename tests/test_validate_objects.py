import pytest

from df_translation_toolkit.validation.validate_objects import validate_brackets


@pytest.mark.parametrize(
    "text, expected",
    [
        ("[text]", True),
        ("[text", False),
        ("text]", False),
        ("[text[]", False),
    ],
)
def test_validate_brackets(text, expected):
    assert validate_brackets(text) == expected
