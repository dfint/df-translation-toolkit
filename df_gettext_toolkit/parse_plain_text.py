from typing import Iterable, Tuple


def skip_tags(s):
    opened = 0
    for char in s:
        if char == '[':
            opened += 1
        elif char == ']':
            opened -= 1
        elif opened == 0:
            yield char


def parse_plain_text_file(lines: Iterable[str], join_paragraphs=True, start_line=1)\
        -> Iterable[Tuple[str, bool, int]]:
    def local_is_translatable(s):
        return any(char.islower() for char in skip_tags(s))

    lines = iter(lines)

    paragraph = ''

    # FIXME: join_paragraphs must only affect on paragraph joining, not line skipping
    # so the first line must be skipped before the text is fed to the function
    if join_paragraphs:
        line = next(lines)  # The first line contains file name, skip it
        yield line, False, 1
        start_line += 1

    paragraph_start_line = start_line

    for line_number, line in enumerate(lines, start_line):
        if join_paragraphs:
            if local_is_translatable(line):
                if '~' in line or line[0] == '[' and not (paragraph and paragraph.rstrip()[-1].isalpha()):
                    if paragraph:
                        yield paragraph, True, paragraph_start_line
                        paragraph = ''
                        paragraph_start_line = line_number

                    if line.rstrip().endswith(']'):
                        yield line, True, line_number
                    else:
                        paragraph += line
                else:
                    paragraph += line
            else:
                if paragraph:
                    yield paragraph, True, paragraph_start_line
                    paragraph = ''
                    paragraph_start_line = line_number

                yield line, False, line_number  # Not translatable line
        else:
            yield line, local_is_translatable(line), line_number

    if paragraph:
        yield paragraph, True, paragraph_start_line