import ast
import re
from collections.abc import Iterable
from typing import NamedTuple

from df_translation_toolkit.parse.parse_plain_text import skip_tags
from df_translation_toolkit.utils.po_utils import TranslationItem

IGNORED_STRINGS = {"cond", "glitchstuff", "buggy", "glitch demon:glitch demons:glitch demon", "unique"}
IGNORED_LINE_STARTS = (
    "require ",
    "require(",
    "get_debug_logger(",
    "o(",
    "l(",
    "l1(",
    "l2(",
    "l3(",
    "l4(",
    "l5(",
    "log(",
    "res.info=",
)


class LuaFileToken(NamedTuple):
    text: str
    is_translatable: bool
    line_number: int
    context: str | None
    comment: str | None
    line: str


def is_translatable(text: str) -> bool:
    if re.match(r"\w+\d+", text):
        return False

    if re.search(r"[a-z]+_[a-z]+", text):
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
        # Remove line comments
        if "--" in line:
            line = line.partition("--")[0]  # noqa: PLW2901

        # TODO(@insolor): Handle block comments properly

        # Ignored lines
        stripped = line.strip()
        if not stripped or stripped.startswith(IGNORED_LINE_STARTS):
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
        result = re.finditer(r"([~=]=\s*)?(\".*?\")", line)
        for item in result:
            is_condition = bool(item.group(1))
            text = ast.literal_eval(item.group(2))
            comment = line.strip().rstrip(",")
            yield LuaFileToken(
                text=text,
                is_translatable=not is_condition and is_translatable(text),
                line_number=line_number,
                line=line,
                comment=comment,
                context=context,
            )


def extract_translatables_from_lua_file(
    lines: Iterable[str],
    *,
    start_line: int = 1,
) -> Iterable[TranslationItem]:
    for item in parse_lua_file(lines, start_line=start_line):
        if not item.is_translatable:
            continue

        yield TranslationItem(
            context=item.context,
            text=item.text,
            extracted_comment=item.comment,
            line_number=item.line_number,
        )
