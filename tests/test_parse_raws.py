import io
from collections.abc import Callable, Mapping, Sequence
from typing import TypeVar

import pytest

from df_translation_toolkit.parse.parse_raws import extract_translatables_from_raws, last_suitable, translate_raw_file
from df_translation_toolkit.utils.po_utils import TranslationItem
from tests.strip_margin import strip_margin


@pytest.mark.parametrize(
    "content, expected",
    [
        (
            strip_margin(
                """
                |creature_birds - file title is ignored
                |[OBJECT:CREATURE]
                |[CREATURE:BIRD_BLUEJAY] - context will be changed to CREATURE:BIRD_BLUEJAY
                |[DESCRIPTION:A small blue-crested bird living in temperate woodlands, known for its harsh chirps.]
                |[NAME:blue jay:blue jays:blue jay]
                |[CASTE_NAME:blue jay:blue jays:blue jay]
                |[GENERAL_CHILD_NAME:blue jay hatchling:blue jay hatchlings]
                |[CREATURE_TILE:144][COLOR:1:0:1]
                |[BIOME:GRASSLAND_TEMPERATE]
                |
                |[CREATURE:BIRD_CARDINAL] - context will be changed to CREATURE:BIRD_CARDINAL
                |[DESCRIPTION:A small bright red bird with a distinctive crest, found in temperate forests.]
                |[NAME:cardinal:cardinals:cardinal]
                |[CASTE_NAME:cardinal:cardinals:cardinal]
                |[GENERAL_CHILD_NAME:cardinal hatchling:cardinal hatchlings]
                |[CREATURE_TILE:144][COLOR:4:0:1]
                |[PETVALUE:30][NATURAL][PET]
                """,
            ).strip(),
            [
                TranslationItem(
                    context="CREATURE:BIRD_BLUEJAY",
                    text=(
                        "[DESCRIPTION:"
                        "A small blue-crested bird living in temperate woodlands, known for its harsh chirps.]"
                    ),
                ),
                TranslationItem(context="CREATURE:BIRD_BLUEJAY", text="[NAME:blue jay:blue jays:blue jay]"),
                TranslationItem(context="CREATURE:BIRD_BLUEJAY", text="[CASTE_NAME:blue jay:blue jays:blue jay]"),
                TranslationItem(
                    context="CREATURE:BIRD_BLUEJAY",
                    text="[GENERAL_CHILD_NAME:blue jay hatchling:blue jay hatchlings]",
                ),
                TranslationItem(
                    context="CREATURE:BIRD_CARDINAL",
                    text="[DESCRIPTION:A small bright red bird with a distinctive crest, found in temperate forests.]",
                ),
                TranslationItem(context="CREATURE:BIRD_CARDINAL", text="[NAME:cardinal:cardinals:cardinal]"),
                TranslationItem(context="CREATURE:BIRD_CARDINAL", text="[CASTE_NAME:cardinal:cardinals:cardinal]"),
                TranslationItem(
                    context="CREATURE:BIRD_CARDINAL",
                    text="[GENERAL_CHILD_NAME:cardinal hatchling:cardinal hatchlings]",
                ),
            ],
        ),
        (
            strip_margin(
                """
                |item_weapon
                |[OBJECT:ITEM]
                |[ITEM_WEAPON:ITEM_WEAPON_WHIP]
                |[NAME:whip:whips]
                |[SIZE:100]
                |[SKILL:WHIP]
                |[TWO_HANDED:27500]
                |[MINIMUM_SIZE:22500]
                |[MATERIAL_SIZE:1]
                |[ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:5000] - 5000 is not translatable
                |    [ATTACK_PREPARE_AND_RECOVER:4:4]
                |    [ATTACK_FLAG_BAD_MULTIATTACK]
                """,
            ).strip(),
            [
                TranslationItem(context="ITEM_WEAPON:ITEM_WEAPON_WHIP", text="[NAME:whip:whips]"),
                TranslationItem(
                    context="ITEM_WEAPON:ITEM_WEAPON_WHIP",
                    text="[ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:]",
                ),
            ],
        ),
        (
            strip_margin(
                """
                |body_default
                |
                |[OBJECT:BODY]
                |
                |[BODY:BASIC_1PARTBODY]
                |    Categories are user-defined strings that can be used elsewhere to refer to groups of bodyparts for other commands.
                |    [BP:UB:body:bodies][UPPERBODY][LOWERBODY][CATEGORY:BODY]
                |    This command establishes the relative size of body parts within a creature.  The numbers have no absolute meaning or units.
                |        [DEFAULT_RELSIZE:2000]
                |
                |[BODY:BASIC_1PARTBODY_THOUGHT]
                |    This is useful for blobs and other simple headless creatures that don't have brains, since they will die then when they lose a functional tissue in this part.
                |    [BP:UB:body:bodies][UPPERBODY][LOWERBODY][THOUGHT][CATEGORY:BODY]
                |        [DEFAULT_RELSIZE:2000]
                |
                |[BODY:BASIC_1PARTBODY_FLYING_HEAD_FLAG_THOUGHT]
                |    [BP:UB:body:bodies][UPPERBODY][LOWERBODY][HEAD][THOUGHT][CATEGORY:BODY][FLIER]
                |        [DEFAULT_RELSIZE:2000]
                |    [BP:UB:body:bodies][UPPERBODY][LOWERBODY][HEAD][THOUGHT][CATEGORY:BODY][FLIER]  # Duplicate entry - must be ignored
                |        [DEFAULT_RELSIZE:2000]
                """,
            ).strip(),
            [
                TranslationItem(context="BODY:BASIC_1PARTBODY", text="[BP:UB:body:bodies]"),
                TranslationItem(context="BODY:BASIC_1PARTBODY_THOUGHT", text="[BP:UB:body:bodies]"),
                TranslationItem(context="BODY:BASIC_1PARTBODY_FLYING_HEAD_FLAG_THOUGHT", text="[BP:UB:body:bodies]"),
            ],
        ),
    ],
)
def test_extract_translatables_from_raws(content: str, expected: list[TranslationItem]) -> None:
    assert list(extract_translatables_from_raws(content.splitlines())) == expected


@pytest.mark.parametrize(
    "content,dictionary,result",
    [
        (
            strip_margin(
                """
                |    item_weapon
                |        [OBJECT:ITEM]
                |            [ITEM_WEAPON:ITEM_WEAPON_WHIP]
                |                [NAME:whip:whips]
                |                    [SIZE:100]
                |                    [SKILL:WHIP]
                |                    [TWO_HANDED:27500]
                |                    [MINIMUM_SIZE:22500]
                |                    Some comment
                |                    [MATERIAL_SIZE:1]  trailing comments are trimmed
                |            [ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:5000]
                """,
            ).strip(),
            {
                (
                    "[NAME:whip:whips]",
                    "ITEM_WEAPON:ITEM_WEAPON_WHIP",
                ): "[NAME:pihw:spihw]",
                (
                    "[ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:]",
                    None,
                ): "[ATTACK:BLUNT:1:10:Lash:Lashes:NO_SUB:]",
            },
            strip_margin(
                """
                |    item_weapon
                |        [OBJECT:ITEM]
                |            [ITEM_WEAPON:ITEM_WEAPON_WHIP]
                |                [NAME:pihw:spihw]
                |                    [SIZE:100]
                |                    [SKILL:WHIP]
                |                    [TWO_HANDED:27500]
                |                    [MINIMUM_SIZE:22500]
                |                    Some comment
                |                    [MATERIAL_SIZE:1]
                |            [ATTACK:BLUNT:1:10:Lash:Lashes:NO_SUB:5000]
                """,
            ).strip(),
        ),
    ],
)
def test_translate_raw_file(content: str, dictionary: Mapping[tuple[str, str | None], str], result: str) -> None:
    assert list(translate_raw_file(io.StringIO(content), dictionary)) == result.splitlines()


T = TypeVar("T")


@pytest.mark.parametrize(
    "sequence, function, expected",
    [
        [[1, 1, 1, 1, 1, 0, 0], bool, 5],
        [[1, 1, 1, 1, 1, 1, 1], bool, 7],
        [[0, 0, 0, 0, 0, 0, 0], bool, 0],
        [[1, 0, 0, 0, 0, 0, 0], bool, 1],
        [[1, 1, 0, 0, 0, 0, 0], bool, 2],
        [[], bool, 0],
    ],
)
def test_last_suitable(sequence: Sequence[T], function: Callable[[T], bool], expected: int) -> None:
    assert last_suitable(sequence, function) == expected
    result = last_suitable(sequence, function)
    assert len(sequence[:result]) == result
