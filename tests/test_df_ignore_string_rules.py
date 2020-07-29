from df_gettext_toolkit.df_ignore_string_rules import *


def test_ignore_xml():
    assert ignore_xml("""<?xml version="1.0" encoding='CP437'?>""") is True
    assert ignore_xml("No love   <->    Loves easily") is False
    assert ignore_xml("<local_id>") is True
    assert ignore_xml("</local_id>") is True
    assert ignore_xml("<type>mead hall</type>") is True
    assert ignore_xml("<no uniforms>") is False


def test_ignore_square_brackets():
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
    assert ignore_square_brackets(":BP:BY_CATEGORY:ALL:EYE") is True


def test_ignore_paths():
    assert ignore_paths('/stdout.txt') is True
    assert ignore_paths('data/save/current') is True
    assert ignore_paths('data/init/interface.txt') is True
    assert ignore_paths('objects/b_detail_plan_*.txt') is True
    assert ignore_paths('/Resting') is False
    assert ignore_paths('Upright Spear/Spike') is False
    assert ignore_paths('Track/Ramp (NW)') is False
    assert ignore_paths('Unknown Body Group/Relation Token(s): ') is False
    assert ignore_paths('data/save/*.*') is True
    assert ignore_paths('.bmp') is True
    assert ignore_paths('grinding.') is False


def test_ignore_filenames():
    assert ignore_filenames("-detailed.bmp") is True


def test_ignore_underline_separated_words():
    assert ignore_underline_separated_words("index1_11") is True


def test_ignore_dash_prepended_strings():
    assert ignore_dash_prepended_strings('-world_sites_and_pops') is True
    assert ignore_dash_prepended_strings('-site_map-') is True


def test_ignore_by_blacklisted_words():
    assert ignore_by_blacklisted_words("*** Error(s) finalizing the creature ") is True


def test_ignore_camel_case():
    assert ignore_camel_case("InitializeConditionVariable") is True
    assert ignore_camel_case("Initialize") is False
    assert ignore_camel_case("SleepConditionVariableCS") is True
    assert ignore_camel_case("CAPS") is False
    assert ignore_camel_case("RefusedID/") is True
    assert ignore_camel_case("plF") is True


def test_ignore_by_blacklisted_substrings():
    assert ignore_by_blacklisted_substrings('plotter (assassinate) placed out of bounds') is True
    assert ignore_by_blacklisted_substrings('undefined local creature material set to default: ') is True


def test_all_ignore_rules():
    assert all_ignore_rules('any text') is False
    assert all_ignore_rules('Any text') is False
    assert all_ignore_rules('Any text.') is False
    assert all_ignore_rules('Another string: just a tests') is False
