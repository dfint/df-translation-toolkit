from df_gettext_toolkit.parse.parse_raws import all_caps, split_tag


def validate_brackets(tag: str):
    return tag.startswith("[") and tag.endswith("]") and tag.count("[") == 1 and tag.count("]") == 1


def validate_tag(original_tag: str, translation_tag: str):
    assert len(translation_tag) > 2, "Too short or empty translation"
    assert translation_tag.strip() == translation_tag, "Extra spaces at the beginning or at the end of the translation"
    assert validate_brackets(translation_tag), "Wrong tag translation format"

    original_parts = split_tag(original_tag)
    translation_parts = split_tag(translation_tag)
    assert len(original_parts) == len(translation_parts), "Tag parts count mismatch"
    validate_tag_parts(original_parts, translation_parts)


def validate_tag_parts(original_parts: list[str], translation_parts: list[str]):
    for original, translation in zip(original_parts, translation_parts):
        if all_caps(original) or original.isdecimal():
            valid = original == translation or original in ("STP", "NP", "SINGULAR", "PLURAL")
            assert valid, f"Part {original!r} should not be translated"

            if original == "STP":
                assert translation != "STP", (
                    "Replace STP with a translation of the previous word in the tag in a plural form, "
                    "otherwise, the game will create a plural form with adding -s at the end. "
                    "If the translation with adding -s at the end is valid for your language, just ignore this message."
                )
        elif original:
            assert translation, "Translation should not be empty"
