import ast
import re
from collections.abc import Iterable
from typing import NamedTuple

from df_translation_toolkit.parse.parse_plain_text import skip_tags


class LuaFileToken(NamedTuple):
    text: str
    is_translatable: bool
    line_number: int
    comment: str | None
    line: str


def is_translatable(s: str) -> bool:
    if re.match(r"\w+\d+", s):
        return False

    return any(char.islower() for char in skip_tags(s))


def parse_lua_file(
    lines: Iterable[str],
    *,
    start_line: int = 1,
) -> Iterable[LuaFileToken]:
    for line_number, line in enumerate(lines, start_line):
        if line.lstrip().startswith(("require ", "require(", "--", "l2(")):
            yield LuaFileToken(
                text=line,
                is_translatable=False,
                line_number=line_number,
                line=line,
                comment=None,
            )
            continue

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
            )
