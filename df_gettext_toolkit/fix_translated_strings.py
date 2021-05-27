from typing import Optional

from unidecode import unidecode_expect_nonascii as unidecode


def fix_leading_spaces(original_string: str, translation: str, exclusions: set):
    if original_string in exclusions:
        return translation

    if (original_string[0] == ' ' and
            translation[0] != ' ' and
            translation[0] != ','):
        translation = ' ' + translation

    if original_string[0] != ' ' and translation[0] == ' ':
        translation = translation.lstrip()

    return translation


def fix_trailing_spaces(original_string: str, translation: str, exclusions: set):
    if original_string not in exclusions and original_string[-1] == ' ' and translation[-1] != ' ':
        translation += ' '

    return translation


def fix_spaces(original_string: str, translation: str,
               exclusions_leading: Optional[set] = None,
               exclusions_trailing: Optional[set] = None):

    exclusions_leading = exclusions_leading or set()
    exclusions_trailing = exclusions_trailing or set()
    translation = fix_leading_spaces(original_string, translation, exclusions_leading)
    translation = fix_trailing_spaces(original_string, translation, exclusions_trailing)
    return translation


_exclusions = '¿¡'


def fix_unicode_symbols(s: str):
    return ''.join(c if c.isalpha() or c in _exclusions else unidecode(c) for c in s)


_character_translation_table = str.maketrans({
    "\ufeff": None,
    "\u200b": None,
    "—": "-",  # Replace Em Dash with the standard dash (unidecode replaces it with two dash symbols)
})


def cleanup_string(s):
    """
    Cleanup a string from unusual unicode characters (quotes, dashes etc.)
    """
    return fix_unicode_symbols(s.translate(_character_translation_table))
