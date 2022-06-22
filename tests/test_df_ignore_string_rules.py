import pytest

import df_gettext_toolkit.df_ignore_string_rules as rules


@pytest.mark.parametrize(
    "string,ignore",
    [
        ("""<?xml version="1.0" encoding='CP437'?>""", True),
        ("No love   <->    Loves easily", False),
        ("<local_id>", True),
        ("/<local_id>", True),
        ("<type>mead hall</type>", True),
        ("<no uniforms>", False),
    ],
)
def test_ignore_xml(string, ignore):
    assert rules.ignore_xml(string) is ignore


@pytest.mark.parametrize(
    "string,ignore",
    [
        ("We have many drinks to choose from.  [You receive a list.]", False),
        ("[B]", True),
        ("[PRO_SUB]", True),
        ("  [You receive a detailed description.]", False),
        ("[CREATURE:", True),
        ("[C:4:0:1]", True),
        (" [C:7:0:1]and is [C:3:0:0]oblivious to reality", False),
        (" [DONE]", False),
        (" [MORE]", False),
        (" [WITH YOU]", False),
        ("([LIP])", False),
        (r"\t\t[SYN_AFFECTED_CLASS:GENERAL_POISON]", True),
        (r"\t\t[SYN_INJECTED][SYN_CONTACT][SYN_INHALED][SYN_INGESTED]", True),
        ("[STATE_ADJ:ALL_SOLID:frozen ", False),
        ("[STATE_ADJ:ALL_SOLID:", True),
        (":BP:BY_CATEGORY:ALL:EYE", True),
    ],
)
def test_ignore_square_brackets(string, ignore):
    assert rules.ignore_square_brackets(string) is ignore


@pytest.mark.parametrize(
    "string,ignore",
    [
        ("/stdout.txt", True),
        ("data/save/current", True),
        ("data/init/interface.txt", True),
        ("objects/b_detail_plan_*.txt", True),
        ("/Resting", False),
        ("Upright Spear/Spike", False),
        ("Track/Ramp (NW)", False),
        ("Unknown Body Group/Relation Token(s): ", False),
        ("data/save/*.*", True),
        (".bmp", True),
        ("grinding.", False),
    ],
)
def test_ignore_paths(string, ignore):
    assert rules.ignore_paths(string) is ignore


def test_ignore_filenames():
    assert rules.ignore_filenames("-detailed.bmp") is True


def test_ignore_underline_separated_words():
    assert rules.ignore_underline_separated_words("index1_11") is True



@pytest.mark.parametrize(
    "string, ignore",
    [
        ("-world_sites_and_pops", True),
        ("-site_map-", True),
    ]
)
def test_ignore_dash_prepended_strings(string, ignore):
    assert rules.ignore_dash_prepended_strings(string) is ignore


@pytest.mark.parametrize(
    "string, ignore",
    [
        ("*** Error(s) finalizing the creature ", True),
    ]
)
def test_ignore_by_blacklisted_words(string, ignore):
    assert rules.ignore_by_blacklisted_words(string) is ignore


@pytest.mark.parametrize(
    "string,ignore",
    [
        ("InitializeConditionVariable", True),
        ("Initialize", False),
        ("SleepConditionVariableCS", True),
        ("CAPS", False),
        ("RefusedID/", True),
        ("plF", True),
    ],
)
def test_ignore_camel_case(string, ignore):
    assert rules.ignore_camel_case(string) is ignore


@pytest.mark.parametrize(
    "string, ignore",
    [
        ("plotter (assassinate) placed out of bounds", True),
        ("undefined local creature material set to default: ", True)
    ]
)
def test_ignore_by_blacklisted_substrings(string, ignore):
    assert rules.ignore_by_blacklisted_substrings(string) is ignore


@pytest.mark.parametrize(
    "string, ignore",
    [
        ("any text", False),
        ("Any text", False),
        ("Any text.", False),
        ("Another string: just a test", False),
    ]
)
def test_all_ignore_rules(string, ignore):
    assert rules.all_ignore_rules(string) is ignore
