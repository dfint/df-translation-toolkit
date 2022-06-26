from typing import Iterable, List, NamedTuple


def skip_tags(s):
    opened = 0
    for char in s:
        if char == "[":
            opened += 1
        elif char == "]":
            opened -= 1
        elif opened == 0:
            yield char


class PlainTextFileToken(NamedTuple):
    test: str
    is_translatable: bool
    line_number: int


def parse_plain_text_file(lines: Iterable[str], join_paragraphs=True, start_line=1) -> Iterable[PlainTextFileToken]:
    def local_is_translatable(s):
        return any(char.islower() for char in skip_tags(s))

    lines = iter(lines)

    paragraph: List[str] = []

    # FIXME: join_paragraphs must only affect on paragraph joining, not line skipping
    # so the first line must be skipped before the text is fed to the function
    if join_paragraphs:
        # The first line contains file name, skip it
        yield PlainTextFileToken(next(lines), False, start_line)
        start_line += 1

    paragraph_start_line = start_line

    for line_number, line in enumerate(lines, start_line):
        if join_paragraphs:
            if local_is_translatable(line):
                if "~" in line or line[0] == "[" and not (paragraph and paragraph[-1][-1].isalpha()):
                    if paragraph:
                        yield PlainTextFileToken(join_paragraph(paragraph), True, paragraph_start_line)
                        paragraph = []
                        paragraph_start_line = line_number

                    if line.rstrip().endswith("]"):
                        yield PlainTextFileToken(line, True, line_number)
                    else:
                        paragraph.append(line)
                else:
                    paragraph.append(line)
            else:
                if paragraph:
                    yield PlainTextFileToken(join_paragraph(paragraph), True, paragraph_start_line)
                    paragraph = []
                    paragraph_start_line = line_number

                yield PlainTextFileToken(line, False, line_number)  # Not translatable line
        else:
            yield PlainTextFileToken(line, local_is_translatable(line), line_number)

    if paragraph:
        yield PlainTextFileToken(join_paragraph(paragraph), True, paragraph_start_line)


def join_paragraph(paragraph):
    return "\n".join(paragraph)
