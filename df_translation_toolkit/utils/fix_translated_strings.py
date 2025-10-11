from unidecode import unidecode_expect_nonascii as unidecode


def fix_leading_spaces(original_string: str, translation: str, *, strict: bool = False) -> str:
    """
    Adds missing space in the beginning of the translation.
    Removes extra spaces, if the translation starts with "." or ",".
    """
    if original_string.startswith(" "):
        if not translation.startswith(" "):
            translation = " " + translation
    elif strict:
        translation = translation.lstrip()

    if translation.lstrip().startswith((".", ",")):
        translation = translation.lstrip()

    return translation


def fix_trailing_spaces(original_string: str, translation: str, *, strict: bool = False) -> str:
    """
    Adds a missing trailing space.
    """
    if original_string.endswith(" "):
        if not translation.endswith(" "):
            translation += " "
    elif strict:
        translation = translation.rstrip()

    return translation


def fix_spaces(original_string: str, translation: str, *, strict: bool = False) -> str:
    """
    Fixes leading and trailing spaces of the translation string
    """
    translation = fix_leading_spaces(original_string, translation, strict=strict)
    return fix_trailing_spaces(original_string, translation, strict=strict)


_exclusions = "¿¡"


def fix_unicode_symbols(s: str) -> str:
    return "".join(c if c.isalpha() or c in _exclusions else unidecode(c) for c in s)


_character_translation_table = str.maketrans(
    {
        "\ufeff": None,
        "\u200b": None,
        "—": "-",  # Replace Em Dash with the standard dash (unidecode replaces it with two dash symbols)
    },
)


def cleanup_string(s: str) -> str:
    """
    Cleanup a string from unusual unicode characters (quotes, dashes etc.)
    """
    return fix_unicode_symbols(s.translate(_character_translation_table))
