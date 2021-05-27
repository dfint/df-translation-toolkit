from unidecode import unidecode_expect_nonascii as unidecode


def fix_spaces(original, translation):
    if len(original) <= 1:
        return translation

    # Fix leading spaces
    if not original.startswith('  ') and original[0] == ' ' and translation[0] not in ' ,':
        translation = ' ' + translation

    # Fix trailing spaces
    if not original.endswith('  ') and original[-1] == ' ' and translation[-1] != ' ':
        translation += ' '

    return translation


def fix_unicode_symbols(s: str):
    return ''.join(c if c.isalpha() else unidecode(c) for c in s)


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
