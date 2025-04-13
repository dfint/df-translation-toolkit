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
def test_validate_brackets(text: str, expected: bool) -> None:  # noqa: FBT001
    assert validate_brackets(text) == expected
