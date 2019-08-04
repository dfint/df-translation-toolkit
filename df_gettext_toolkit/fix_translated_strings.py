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


def cleanup_string(s):
    """Cleanup a string from unusual unicode characters (quotes, dashes etc.)"""
    return s.translate({0xfeff: None, 0x2019: "'", 0x201d: '"', 0x2013: '-'})
