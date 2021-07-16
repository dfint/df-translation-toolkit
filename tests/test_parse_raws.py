import io

import pytest

from df_gettext_toolkit.parse_raws import extract_translatables_from_raws, translate_raw_file


@pytest.mark.parametrize(
    "content,result",
    [
        (
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
                """.splitlines(),
                [('CREATURE:BIRD_BLUEJAY',
                  '[DESCRIPTION:A small blue-crested bird living in temperate woodlands, known for its harsh chirps.]',
                  5),
                 ('CREATURE:BIRD_BLUEJAY', '[NAME:blue jay:blue jays:blue jay]', 6),
                 ('CREATURE:BIRD_BLUEJAY', '[CASTE_NAME:blue jay:blue jays:blue jay]', 7),
                 ('CREATURE:BIRD_BLUEJAY', '[GENERAL_CHILD_NAME:blue jay hatchling:blue jay hatchlings]', 8),
                 ('CREATURE:BIRD_CARDINAL',
                  '[DESCRIPTION:A small bright red bird with a distinctive crest, found in '  'temperate forests.]',
                  13), ('CREATURE:BIRD_CARDINAL', '[NAME:cardinal:cardinals:cardinal]', 14),
                 ('CREATURE:BIRD_CARDINAL', '[CASTE_NAME:cardinal:cardinals:cardinal]', 15),
                 ('CREATURE:BIRD_CARDINAL', '[GENERAL_CHILD_NAME:cardinal hatchling:cardinal hatchlings]', 16)]
        ),
        (
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
                """.splitlines(),
                [('ITEM_WEAPON:ITEM_WEAPON_WHIP', '[NAME:whip:whips]', 5),
                 ('ITEM_WEAPON:ITEM_WEAPON_WHIP', '[ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:]', 11)]
        )
    ]
)
def test_extract_translatables_from_raws(content, result):
    assert list(extract_translatables_from_raws(content)) == result


@pytest.mark.parametrize(
    "content,dictionary,result", [
        (
                "item_weapon\n"
                "    [OBJECT:ITEM]\n"
                "        [ITEM_WEAPON:ITEM_WEAPON_WHIP]\n"
                "            [NAME:whip:whips]\n"
                "                [SIZE:100]\n"
                "                [SKILL:WHIP]\n"
                "                [TWO_HANDED:27500]\n"
                "                [MINIMUM_SIZE:22500]\n"
                "                Some comment\n"
                "                [MATERIAL_SIZE:1]  trailing comments are trimmed\n"
                "        [ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:5000]",
                {
                    ("[NAME:whip:whips]", "ITEM_WEAPON:ITEM_WEAPON_WHIP"): "[NAME:pihw:spihw]",
                    ("[ATTACK:BLUNT:1:10:lash:lashes:NO_SUB:]", None): "[ATTACK:BLUNT:1:10:Lash:Lashes:NO_SUB:]"
                },
                "item_weapon\n"
                "    [OBJECT:ITEM]\n"
                "        [ITEM_WEAPON:ITEM_WEAPON_WHIP]\n"
                "            [NAME:pihw:spihw]\n"
                "                [SIZE:100]\n"
                "                [SKILL:WHIP]\n"
                "                [TWO_HANDED:27500]\n"
                "                [MINIMUM_SIZE:22500]\n"
                "                Some comment\n"
                "                [MATERIAL_SIZE:1]\n"
                "        [ATTACK:BLUNT:1:10:Lash:Lashes:NO_SUB:5000]",
        )
    ]
)
def test_translate_raw_file(content, dictionary, result):
    assert list(translate_raw_file(io.StringIO(content), dictionary)) == result.splitlines()