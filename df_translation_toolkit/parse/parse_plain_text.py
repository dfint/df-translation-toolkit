from collections.abc import Iterable, Iterator
from typing import NamedTuple


def skip_tags(s: str) -> Iterator[str]:
    opened = 0
    for char in s:
        if char == "[":
            opened += 1
        elif char == "]":
            opened -= 1
        elif opened == 0:
            yield char


class PlainTextFileToken(NamedTuple):
    text: str
    is_translatable: bool
    line_number: int


def parse_plain_text_file(
    lines: Iterable[str],
    join_paragraphs: bool = True,
    start_line: int = 1,
) -> Iterable[PlainTextFileToken]:
    def local_is_translatable(s: str) -> bool:
        return any(char.islower() for char in skip_tags(s))

    lines = iter(lines)

    paragraph: list[str] = []

    # FIXME(@insolor): join_paragraphs must only affect on paragraph joining, not line skipping
    # so the first line must be skipped before the text is fed to the function
    if join_paragraphs:
        # The first line contains file name, skip it
        yield PlainTextFileToken(text=next(lines), is_translatable=False, line_number=start_line)
        start_line += 1

    paragraph_start_line = start_line

    for line_number, line in enumerate(lines, start_line):
        if join_paragraphs:
            if local_is_translatable(line):
                if line.startswith("[") and not (paragraph and paragraph[-1][-1].isalpha()):
                    if paragraph:
                        yield PlainTextFileToken(
                            text=join_paragraph(paragraph),
                            is_translatable=True,
                            line_number=paragraph_start_line,
                        )
                        paragraph = []
                        paragraph_start_line = line_number

                    if line.rstrip().endswith("]"):
                        yield PlainTextFileToken(text=line, is_translatable=True, line_number=line_number)
                    else:
                        paragraph.append(line)
                else:
                    paragraph.append(line)
            else:
                if paragraph:
                    yield PlainTextFileToken(
                        text=join_paragraph(paragraph),
                        is_translatable=True,
                        line_number=paragraph_start_line,
                    )
                    paragraph = []
                    paragraph_start_line = line_number

                yield PlainTextFileToken(
                    text=line,
                    is_translatable=False,
                    line_number=line_number,
                )  # Not translatable line
        else:
            yield PlainTextFileToken(text=line, is_translatable=local_is_translatable(line), line_number=line_number)

    if paragraph:
        yield PlainTextFileToken(text=join_paragraph(paragraph), is_translatable=True, line_number=paragraph_start_line)


def join_paragraph(paragraph: Iterable[str]) -> str:
    return "\n".join(paragraph)
