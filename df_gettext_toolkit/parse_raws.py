from typing import Iterable, Iterator, List, Mapping, Tuple, Optional, Sequence, Callable, Set, NamedTuple

from df_gettext_toolkit.common import TranslationItem


def split_tag(s: str) -> List[str]:
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


translatable_tags = {"SINGULAR", "PLURAL", "STP", "NO_SUB", "NP", "NA"}


def is_translatable(string: str) -> bool:
    return string in translatable_tags or any("a" <= char <= "z" for char in string)


def join_tag(tag: Iterable[str]) -> str:
    return "[{}]".format(":".join(tag))


def last_suitable(parts: Sequence[str], func: Callable[[str], bool]) -> int:
    for i in range(len(parts) - 1, 0, -1):
        if func(parts[i]):
            return i + 1  # if the last element is suitable, then return len(s), so that s[:i] gives full list
    else:
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
    context: Optional[str]
    text: Optional[str] = None
    tag: Optional[str] = None
    tag_parts: Optional[Sequence[str]] = None


def parse_raw_file(file: Iterable[str]) -> Iterator[FilePartInfo]:
    object_name = None
    context = None
    for token in tokenize_raw_file(file):
        if not token.is_tag:
            yield FilePartInfo(token.line_number, False, context, text=token.text)
        else:
            tag = token.text
            tag_parts = split_tag(tag)

            if tag_parts[0] == "OBJECT":
                object_name = tag_parts[1]
                yield FilePartInfo(token.line_number, False, context, tag=tag)
            elif object_name and (
                tag_parts[0] == object_name
                or (object_name in {"ITEM", "BUILDING"} and tag_parts[0].startswith(object_name))
                or object_name.endswith("_" + tag_parts[0])
            ):
                context = ":".join(tag_parts)
                yield FilePartInfo(token.line_number, False, context, tag=tag)
            else:
                yield FilePartInfo(token.line_number, True, context, tag=tag, tag_parts=tag_parts)


def extract_translatables_from_raws(file: Iterable[str]) -> Iterator[TranslationItem]:
    translation_keys: Set[Tuple[str, ...]] = set()  # Translation keys in the current context

    for item in parse_raw_file(file):
        if item.translatable:
            tag_parts = item.tag_parts
            if (
                "TILE" not in tag_parts[0]
                and any(is_translatable(s) for s in tag_parts[1:])
                and tuple(tag_parts) not in translation_keys  # Don't add duplicate items to translate
            ):
                if not is_translatable(tag_parts[-1]):
                    last = last_suitable(tag_parts, is_translatable)
                    tag_parts = tag_parts[:last]
                    tag_parts.append("")  # Add an empty element to the tag to mark the tag as not completed
                translation_keys.add(tuple(tag_parts))
                yield TranslationItem(context=item.context, text=join_tag(tag_parts), line_number=item.line_number)


def translate_raw_file(file: Iterable[str], dictionary: Mapping[Tuple[str, Optional[str]], str]):
    prev_line_number = 1
    modified_line_parts = []
    for item in parse_raw_file(file):
        if item.line_number > prev_line_number:
            yield "".join(modified_line_parts)
            modified_line_parts = []

        prev_line_number = item.line_number

        if item.text:
            modified_line_parts.append(item.text)
        elif not item.translatable or not any(is_translatable(s) for s in item.tag_parts[1:]):
            modified_line_parts.append(item.tag)
        else:
            tag = item.tag
            tag_parts = item.tag_parts
            context = item.context

            if (tag, item.context) in dictionary:
                tag = dictionary[(tag, item.context)]
            elif (tag, None) in dictionary:
                tag = dictionary[(tag, None)]
            elif not is_translatable(tag_parts[-1]):
                last = last_suitable(tag_parts, is_translatable)
                translatable_tag_parts = tag_parts[:last]
                translatable_tag_parts.append("")

                tag_key = join_tag(translatable_tag_parts)

                new_tag_parts = None
                if (tag_key, context) in dictionary:
                    new_tag_parts = split_tag(dictionary[(tag_key, context)])
                elif (tag_key, None) in dictionary:
                    new_tag_parts = split_tag(dictionary[(tag_key, None)])

                if new_tag_parts:
                    tag_parts[: len(new_tag_parts) - 1] = new_tag_parts[:-1]
                    tag = join_tag(tag_parts)

            modified_line_parts.append(tag)

    if modified_line_parts:
        yield "".join(modified_line_parts)
