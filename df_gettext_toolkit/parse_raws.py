from typing import List, Iterator, Iterable


def split_tag(s: str) -> List[str]:
    return s.strip("[]").split(":")


def iterate_tags(s: str) -> Iterator[List[str]]:
    tag_start = None
    for i, char in enumerate(s):
        if tag_start is None:
            if char == "[":
                tag_start = i
            else:
                pass
        elif char == "]":
            yield split_tag(s[tag_start:i])
            tag_start = None


translatable_tags = {"SINGULAR", "PLURAL", "STP", "NO_SUB", "NP", "NA"}


def is_translatable(s):
    return s in translatable_tags or any("a" <= char <= "z" for char in s)


def join_tag(tag):
    return "[%s]" % ":".join(tag)


def last_suitable(s, func):
    for i in range(len(s) - 1, 0, -1):
        if func(s[i]):
            return i + 1  # if the last element is suitable, then return len(s), so that s[:i] gives full list
    else:
        return 0  # if there aren't suitable elements, then return 0, so that s[:i] gives empty list


def extract_translatables_from_raws(file: Iterable[str]):
    obj = None
    context = None
    keys = set()
    for i, line in enumerate(file, 1):
        for tag_parts in iterate_tags(line):
            if tag_parts[0] == "OBJECT":
                obj = tag_parts[1]
            elif obj and (
                tag_parts[0] == obj
                or (obj in {"ITEM", "BUILDING"} and tag_parts[0].startswith(obj))
                or obj.endswith("_" + tag_parts[0])
            ):
                context = ":".join(tag_parts)  # don't enclose context string into brackets - transifex dislikes this
                keys.clear()
            elif (
                "TILE" not in tag_parts[0]
                and any(is_translatable(s) for s in tag_parts[1:])
                and tuple(tag_parts) not in keys
            ):
                if not is_translatable(tag_parts[-1]):
                    last = last_suitable(tag_parts, is_translatable)
                    tag_parts = tag_parts[:last]
                    tag_parts.append("")  # Add an empty element to the tag to mark the tag as not completed
                keys.add(tuple(tag_parts))
                yield context, join_tag(tag_parts), i


def translate_raw_file(file, dictionary):
    obj = None
    context = None
    for line in file:
        if "[" in line:
            modified_line = line.partition("[")[0]
            for tag_parts in iterate_tags(line):
                if tag_parts[0] == "OBJECT":
                    obj = tag_parts[1]
                elif obj and (
                    tag_parts[0] == obj
                    or (obj in {"ITEM", "BUILDING"} and tag_parts[0].startswith(obj))
                    or obj.endswith("_" + tag_parts[0])
                ):
                    context = ":".join(tag_parts)

                tag = join_tag(tag_parts)
                if any(is_translatable(s) for s in tag_parts[1:]):
                    key = (tag, context)
                    if key in dictionary:
                        tag = dictionary[key]
                    elif (tag, None) in dictionary:
                        tag = dictionary[(tag, None)]
                    elif not is_translatable(tag_parts[-1]):
                        last = last_suitable(tag_parts, is_translatable)
                        new_tag = tag_parts[: last + 1]
                        new_tag[-1] = ""
                        tag = join_tag(new_tag)
                        key = (tag, context)
                        new_tag = None
                        if key in dictionary:
                            new_tag = split_tag(dictionary[key])
                        elif (tag, None) in dictionary:
                            new_tag = split_tag(dictionary[(tag, None)])

                        if new_tag:
                            tag_parts[: len(new_tag) - 1] = new_tag[:-1]
                            tag = join_tag(tag_parts)

                modified_line += tag
            yield modified_line
        else:
            yield line.rstrip()
