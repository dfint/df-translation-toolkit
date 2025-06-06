from collections.abc import Callable

import pytest

import df_translation_toolkit.utils.df_ignore_string_rules as rules


@pytest.mark.parametrize(
    "rule, string, ignore",
    [
        (rules.ignore_xml, """<?xml version="1.0" encoding='CP437'?>""", True),
        (rules.ignore_xml, "No love   <->    Loves easily", False),
        (rules.ignore_xml, "<local_id>", True),
        (rules.ignore_xml, "/<local_id>", True),
        (rules.ignore_xml, "<type>mead hall</type>", True),
        (rules.ignore_xml, "<no uniforms>", False),
        (
            rules.ignore_square_brackets,
            "We have many drinks to choose from.  [You receive a list.]",
            False,
        ),
        (rules.ignore_square_brackets, "[B]", True),
        (rules.ignore_square_brackets, "[PRO_SUB]", True),
        (
            rules.ignore_square_brackets,
            "  [You receive a detailed description.]",
            False,
        ),
        (rules.ignore_square_brackets, "[CREATURE:", True),
        (rules.ignore_square_brackets, "[C:4:0:1]", True),
        (
            rules.ignore_square_brackets,
            " [C:7:0:1]and is [C:3:0:0]oblivious to reality",
            False,
        ),
        (rules.ignore_square_brackets, " [DONE]", False),
        (rules.ignore_square_brackets, " [MORE]", False),
        (rules.ignore_square_brackets, " [WITH YOU]", False),
        (rules.ignore_square_brackets, "([LIP])", False),
        (
            rules.ignore_square_brackets,
            r"\t\t[SYN_AFFECTED_CLASS:GENERAL_POISON]",
            True,
        ),
        (
            rules.ignore_square_brackets,
            r"\t\t[SYN_INJECTED][SYN_CONTACT][SYN_INHALED][SYN_INGESTED]",
            True,
        ),
        (rules.ignore_square_brackets, "[STATE_ADJ:ALL_SOLID:frozen ", False),
        (rules.ignore_square_brackets, "[STATE_ADJ:ALL_SOLID:", True),
        (rules.ignore_square_brackets, ":BP:BY_CATEGORY:ALL:EYE", True),
        (rules.ignore_paths, "/stdout.txt", True),
        (rules.ignore_paths, "data/save/current", True),
        (rules.ignore_paths, "data/init/interface.txt", True),
        (rules.ignore_paths, "objects/b_detail_plan_*.txt", True),
        (rules.ignore_paths, "/Resting", False),
        (rules.ignore_paths, "Upright Spear/Spike", False),
        (rules.ignore_paths, "Track/Ramp (NW)", False),
        (rules.ignore_paths, "Unknown Body Group/Relation Token(s): ", False),
        (rules.ignore_paths, "data/save/*.*", True),
        (rules.ignore_paths, ".bmp", True),
        (rules.ignore_paths, "grinding.", False),
        (rules.ignore_filenames, "-detailed.bmp", True),
        (rules.ignore_underline_separated_words, "index1_11", True),
        (rules.ignore_underline_separated_words, "_Thrd_id", True),
        (rules.ignore_underline_separated_words, "_initterm_e", True),
        (rules.ignore_underline_separated_words, "init_sound returned false!", True),
        (rules.ignore_dash_separated_words, "piano-pluck-main", True),
        (rules.ignore_dash_separated_words, "gtr-2", True),
        (rules.ignore_dash_separated_words, "clouds-off", True),
        (rules.ignore_dash_prepended_strings, "-world_sites_and_pops", True),
        (rules.ignore_dash_prepended_strings, "-site_map-", True),
        (rules.ignore_dash_prepended_strings, "-beta23", True),
        (
            rules.ignore_by_blacklisted_words,
            "*** Error(s) finalizing the creature ",
            True,
        ),
        (rules.ignore_mixed_case, "InitializeConditionVariable", True),
        (rules.ignore_mixed_case, "Initialize", False),
        (rules.ignore_mixed_case, "SleepConditionVariableCS", True),
        (rules.ignore_mixed_case, "CAPS", False),
        (rules.ignore_mixed_case, "RefusedID/", True),
        (rules.ignore_mixed_case, "plF", True),
        (
            rules.ignore_by_blacklisted_substrings,
            "plotter (assassinate) placed out of bounds",
            True,
        ),
        (
            rules.ignore_by_blacklisted_substrings,
            "undefined local creature material set to default: ",
            True,
        ),
        (rules.all_ignore_rules, "any text", False),
        (rules.all_ignore_rules, "Any text", False),
        (rules.all_ignore_rules, "Any text.", False),
        (rules.all_ignore_rules, "Another string: just a test", False),
        # Translation of these will replace key names
        (rules.all_ignore_rules, "i", True),
        (rules.all_ignore_rules, "a", True),
        (rules.dont_ignore, "", False),
        (rules.all_ignore_rules, "She", False),
        (rules.all_ignore_rules, "she", False),
        (rules.all_ignore_rules, "/N", False),
    ],
)
def test_ignore_rules(rule: Callable[[str], bool], string: str, ignore: bool) -> None:  # noqa: FBT001
    rule_name = rule(string)
    assert bool(rule_name) is ignore, rule_name
