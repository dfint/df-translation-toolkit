import re
from .parse_raws import is_translatable


def ignore_xml(string):
    result = re.search(r"""<(\?xml .*|[\w/]+)>""", string)
    return result is not None


def test_ignore_xml():
    assert ignore_xml("""<?xml version="1.0" encoding='CP437'?>""") is True
    assert ignore_xml("No love   <->    Loves easily") is False
    assert ignore_xml("<local_id>") is True
    assert ignore_xml("</local_id>") is True
    assert ignore_xml("<type>mead hall</type>") is True
    assert ignore_xml("<no uniforms>") is False


square_brackets_exceptions = {'DONE', 'MORE', "CAN'T WORK", "WITH YOU", "LIP"}


def ignore_square_brackets(string):
    if '[' not in string and ']' not in string:
        return False
    string = string.replace(r'\t', '\t')
    parts = re.split(r'[\[:\]]', string)
    return not any(is_translatable(part) or part in square_brackets_exceptions for part in parts)


def test_ignore_square_brackets():
    assert ignore_square_brackets('any string') is False
    assert ignore_square_brackets('We have many drinks to choose from.  [You receive a list.]') is False
    assert ignore_square_brackets('[B]') is True
    assert ignore_square_brackets('[PRO_SUB]') is True
    assert ignore_square_brackets('  [You receive a detailed description.]') is False
    assert ignore_square_brackets('[CREATURE:') is True
    assert ignore_square_brackets('[C:4:0:1]') is True
    assert ignore_square_brackets(' [C:7:0:1]and is [C:3:0:0]oblivious to reality') is False
    assert ignore_square_brackets(' [DONE]') is False
    assert ignore_square_brackets(' [MORE]') is False
    assert ignore_square_brackets(" [CAN'T WORK]") is False
    assert ignore_square_brackets(" [WITH YOU]") is False
    assert ignore_square_brackets("([LIP])") is False
    assert ignore_square_brackets(r"\t\t[SYN_AFFECTED_CLASS:GENERAL_POISON]") is True
    assert ignore_square_brackets(r"\t\t[SYN_INJECTED][SYN_CONTACT][SYN_INHALED][SYN_INGESTED]") is True
    assert ignore_square_brackets("[STATE_ADJ:ALL_SOLID:frozen ") is False
    assert ignore_square_brackets("[STATE_ADJ:ALL_SOLID:") is True


all_rules = [ignore_xml, ignore_square_brackets]


def ignore_all(string):
    return any(rule(string) for rule in all_rules)
