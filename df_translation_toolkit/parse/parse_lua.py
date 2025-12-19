import ast
import re
from collections.abc import Iterable
from typing import NamedTuple

from df_translation_toolkit.parse.parse_plain_text import skip_tags


class LuaFileToken(NamedTuple):
    text: str
    is_translatable: bool
    line_number: int
    context: str | None
    comment: str | None
    line: str


IGNORED_STRINGS = {"cond", "glitchstuff"}


def is_translatable(text: str) -> bool:
    if re.match(r"\w+\d+", text):
        return False

    if text in IGNORED_STRINGS:
        return False

    return any(char.islower() for char in skip_tags(text))


def parse_lua_file(
    lines: Iterable[str],
    *,
    start_line: int = 1,
) -> Iterable[LuaFileToken]:
    context = None
    nesting_level = 0
    for line_number, line in enumerate(lines, start_line):
        # Ignored lines
        if line.lstrip().startswith(("require ", "require(", "--", "l2(")):
            yield LuaFileToken(
                text=line,
                is_translatable=False,
                line_number=line_number,
                line=line,
                comment=None,
                context=None,
            )
            continue

        # End context
        if context:
            nesting_level += line.count("{") - line.count("}")

            if nesting_level <= 0:
                context = None

        # Start context
        context_line = re.fullmatch(r"\s*([\w\.]+)\s*=\s*{\s", line)
        if context_line:
            context = context_line.group(1)
            nesting_level = 1
            continue

        # Translatable parts
        result = re.finditer(r"((\w+)\s*=\s*)?(\".*?\")", line)
        for item in result:
            text = ast.literal_eval(item.group(3))
            comment = item.group(2) or line.strip()
            yield LuaFileToken(
                text=text,
                is_translatable=is_translatable(text),
                line_number=line_number,
                line=line,
                comment=comment,
                context=context,
            )
