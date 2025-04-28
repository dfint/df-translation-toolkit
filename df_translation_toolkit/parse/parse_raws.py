from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import NamedTuple, TypeVar

from df_translation_toolkit.utils.po_utils import TranslationItem


def all_caps(string: str) -> bool:
    return len(string) > 1 and string.isupper()


def split_tag(s: str) -> list[str]:
    return s.strip("[]").split(":")


def iterate_tags(s: str) -> Iterator[str]:
    tag_start = None
    for i, char in enumerate(s):
        if tag_start is None:
            if char == "[":
                tag_start = i
        elif char == "]":
            yield s[tag_start : i + 1]
            tag_start = None


translatable_tags = {"SINGULAR", "PLURAL", "STP", "NO_SUB", "NP"}


def is_translatable(string: str) -> bool:
    return string in translatable_tags or (any("a" <= char <= "z" for char in string) and string != "n/a")


def join_tag(tag: Iterable[str]) -> str:
    return "[{}]".format(":".join(tag))


T = TypeVar("T")


def last_suitable(parts: Sequence[T], func: Callable[[T], bool]) -> int:
    for i in range(len(parts) - 1, -1, -1):
        if func(parts[i]):
            return i + 1  # if the last element is suitable, then return len(s), so that s[:i] gives full list
    return 0  # if there aren't suitable elements, then return 0, so that s[:i] gives empty list


class RawFileToken(NamedTuple):
    line_number: int
    is_tag: bool
    text: str


def tokenize_raw_file(file: Iterable[str]) -> Iterator[RawFileToken]:
    for i, line in enumerate(file, 1):
        if "[" not in line:
            yield RawFileToken(i, is_tag=False, text=line.rstrip())
        else:
            line_start = line.partition("[")[0]
            yield RawFileToken(i, is_tag=False, text=line_start)
            yield from (RawFileToken(i, is_tag=True, text=tag) for tag in iterate_tags(line))


class FilePartInfo(NamedTuple):
    line_number: int
    translatable: bool
    context: str | None
    text: str = ""
    tag: str = ""
    tag_parts: Sequence[str] = ()


def parse_raw_file(file: Iterable[str]) -> Iterator[FilePartInfo]:
    object_name = None
    context = None
    for token in tokenize_raw_file(file):
        if not token.is_tag:
            yield FilePartInfo(line_number=token.line_number, translatable=False, context=context, text=token.text)
            continue

        tag = token.text
        tag_parts = split_tag(tag)

        if tag_parts[0] == "OBJECT":
            object_name = tag_parts[1]
            yield FilePartInfo(line_number=token.line_number, translatable=False, context=context, tag=tag)
        elif object_name and (
            tag_parts[0] == object_name
            or (object_name in {"ITEM", "BUILDING"} and tag_parts[0].startswith(object_name))
            or object_name.endswith("_" + tag_parts[0])
        ):
            context = ":".join(tag_parts)
            yield FilePartInfo(token.line_number, translatable=False, context=context, tag=tag)
        else:
            yield FilePartInfo(token.line_number, translatable=True, context=context, tag=tag, tag_parts=tag_parts)


def extract_translatables_from_raws(file: Iterable[str]) -> Iterator[TranslationItem]:
    translation_keys: set[tuple[str | None, tuple[str, ...]]] = set()

    for item in parse_raw_file(file):
        if not item.translatable:
            continue

        tag_parts = item.tag_parts
        if (
            "TILE" not in tag_parts[0]
            and any(is_translatable(s) for s in tag_parts[1:])
            and (item.context, tuple(tag_parts)) not in translation_keys  # Don't add duplicate items to translate
        ):
            if not is_translatable(tag_parts[-1]):
                last = last_suitable(tag_parts, is_translatable)
                tag_parts = list(tag_parts[:last])
                tag_parts.append("")  # Add an empty element to the tag to mark the tag as not completed
            translation_keys.add((item.context, tuple(tag_parts)))
            yield TranslationItem(context=item.context, text=join_tag(tag_parts))


def get_from_dict_with_context(
    dictionary: Mapping[tuple[str, str | None], str],
    key: str,
    context: str | None,
) -> str | None:
    if (key, context) in dictionary:
        return dictionary[(key, context)]

    if (key, None) in dictionary:
        return dictionary[(key, None)]

    return None


def get_tag_translation(dictionary: Mapping[tuple[str, str | None], str], item: FilePartInfo) -> str:
    tag = item.tag
    tag_parts = list(item.tag_parts)
    context = item.context
    new_tag = get_from_dict_with_context(dictionary, tag, context)

    if new_tag:
        tag = new_tag
    elif not is_translatable(tag_parts[-1]):
        last = last_suitable(tag_parts, is_translatable)
        translatable_tag_parts = tag_parts[:last]
        translatable_tag_parts.append("")

        tag_key = join_tag(translatable_tag_parts)

        new_tag = get_from_dict_with_context(dictionary, tag_key, context)

        if new_tag:
            new_tag_parts = split_tag(new_tag)
            tag_parts[: len(new_tag_parts) - 1] = new_tag_parts[:-1]
            tag = join_tag(tag_parts)

    return tag


def translate_raw_file(file: Iterable[str], dictionary: Mapping[tuple[str, str | None], str]) -> Iterator[str]:
    prev_line_number = 1
    modified_line_parts: list[str] = []
    for item in parse_raw_file(file):
        if item.line_number > prev_line_number:
            yield "".join(modified_line_parts)
            modified_line_parts = []
            prev_line_number = item.line_number

        if item.text:
            modified_line_parts.append(item.text)
        elif item.translatable and any(is_translatable(s) for s in item.tag_parts[1:]):
            translation = get_tag_translation(dictionary, item)
            modified_line_parts.append(translation)
        else:
            modified_line_parts.append(item.tag)

    if modified_line_parts:
        yield "".join(modified_line_parts)
