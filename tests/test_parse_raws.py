import io
from inspect import cleandoc as trim_indent

import pytest

from df_gettext_toolkit import PoItem
from df_gettext_toolkit.parse_raws import (
    extract_translatables_from_raws,
    translate_raw_file,
)


@pytest.mark.parametrize(
    "content, expected",
    [
        (
            trim_indent(
                """
                creature_birds - file title is ignored
                [OBJECT:CREATURE]
                [CREATURE:BIRD_BLUEJAY] - context will be changed to CREATURE:BIRD_BLUEJAY
                [DESCRIPTION:A small blue-crested bird living in temperate woodlands, known for its harsh chirps.]
                [NAME:blue jay:blue jays:blue jay]
                [CASTE_NAME:blue jay:blue jays:blue jay]
                [GENERAL_CHILD_NAME:blue jay hatchling:blue jay hatchlings]
                [CREATURE_TILE:144][COLOR:1:0:1]
                [BIOME:GRASSLAND_TEMPERATE]
                
                [CREATURE:BIRD_CARDINAL] - context will be changed to CREATURE:BIRD_CARDINAL
                [DESCRIPTION:A small bright red bird with a distinctive crest, found in temperate forests.]
                [NAME:cardinal:cardinals:cardinal]
                [CASTE_NAME:cardinal:cardinals:cardinal]
                [GENERAL_CHILD_NAME:cardinal hatchling:cardinal hatchlings]
                [CREATURE_TILE:144][COLOR:4:0:1]
                [PETVALUE:30][NATURAL][PET]
                """
            ).splitlines(),
            [
                PoItem(
                    context="CREATURE:BIRD_BLUEJAY",
                    text=(
                        "[DESCRIPTION:"
                        "A small blue-crested bird living in temperate woodlands, known for its harsh chirps.]"
                    ),
                ),
                PoItem(context="CREATURE:BIRD_BLUEJAY", text="[NAME:blue jay:blue jays:blue jay]"),
                PoItem(context="CREATURE:BIRD_BLUEJAY", text="[CASTE_NAME:blue jay:blue jays:blue jay]"),
                PoItem(
                    context="CREATURE:BIRD_BLUEJAY",
                    text="[GENERAL_CHILD_NAME:blue jay hatchling:blue jay hatchlings]",
                ),
                PoItem(
                    context="CREATURE:BIRD_CARDINAL",
                    text="[DESCRIPTION:A small bright red bird with a distinctive crest, found in temperate forests.]",
                ),
                PoItem(context="CREATURE:BIRD_CARDINAL", text="[NAME:cardinal:cardinals:cardinal]"),
                PoItem(context="CREATURE:BIRD_CARDINAL", text="[CASTE_NAME:cardinal:cardinals:cardinal]"),
                PoItem(
                    context="CREATURE:BIRD_CARDINAL",
                    text="[GENERAL_CHILD_NAME:cardinal hatchling:cardinal hatchlings]",
                ),
            ],
        ),
        (
            trim_indent(
                """
                item_weapon
                [OBJECT:ITEM]
                [ITEM_WEAPON:ITEM_WEAPON_WHIP]
                [NAME:whip:whips]
                [SIZE:100]
                [SKILL:WHIP]
                [TWO_HANDED:27500]
                [MINIMUM_SIZE:22500]
                [MATERIAL_SIZE:1]
                [ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:5000] - 5000 is not translatable 
                    [ATTACK_PREPARE_AND_RECOVER:4:4]
                    [ATTACK_FLAG_BAD_MULTIATTACK]
                """
            ).splitlines(),
            [
                PoItem(context="ITEM_WEAPON:ITEM_WEAPON_WHIP", text="[NAME:whip:whips]"),
                PoItem(
                    context="ITEM_WEAPON:ITEM_WEAPON_WHIP",
                    text="[ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:]",
                ),
            ],
        ),
    ],
)
def test_extract_translatables_from_raws(content, expected):
    assert list(extract_translatables_from_raws(content)) == expected


@pytest.mark.parametrize(
    "content,dictionary,result",
    [
        (
            trim_indent(
                """
                    item_weapon
                        [OBJECT:ITEM]
                            [ITEM_WEAPON:ITEM_WEAPON_WHIP]
                                [NAME:whip:whips]
                                    [SIZE:100]
                                    [SKILL:WHIP]
                                    [TWO_HANDED:27500]
                                    [MINIMUM_SIZE:22500]
                                    Some comment
                                    [MATERIAL_SIZE:1]  trailing comments are trimmed
                            [ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:5000]"""
            ),
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
            trim_indent(
                """
                    item_weapon
                        [OBJECT:ITEM]
                            [ITEM_WEAPON:ITEM_WEAPON_WHIP]
                                [NAME:pihw:spihw]
                                    [SIZE:100]
                                    [SKILL:WHIP]
                                    [TWO_HANDED:27500]
                                    [MINIMUM_SIZE:22500]
                                    Some comment
                                    [MATERIAL_SIZE:1]
                            [ATTACK:BLUNT:1:10:Lash:Lashes:NO_SUB:5000]"""
            ),
        )
    ],
)
def test_translate_raw_file(content, dictionary, result):
    assert list(translate_raw_file(io.StringIO(content), dictionary)) == result.splitlines()
