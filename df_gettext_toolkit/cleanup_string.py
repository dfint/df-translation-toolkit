
def cleanup(s):
    '''Cleanup a string from unusual unicode characters (quotes, dashes etc.)'''
    return s.translate({0xfeff: None, 0x2019: "'", 0x201d: '"', 0x2013: '-'})
