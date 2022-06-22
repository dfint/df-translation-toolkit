import sys
from pathlib import Path

import typer

from .parse_plain_text import parse_plain_text_file
from .parse_po import format_po


def main(path: Path, split: bool = False):
    join_paragraphs = not split

    keys = set()
    for file_path in sorted(path.rglob("*.txt")):
        if file_path.is_file():
            print(file_path, file=sys.stderr)
            with open(file_path) as file:
                for text_block, is_translatable, line_number in parse_plain_text_file(file, join_paragraphs):
                    if is_translatable:
                        if text_block in keys:
                            print("Key already exists:", repr(text_block), file=sys.stderr)
                        else:
                            keys.add(text_block)
                            print("#: %s:%d" % (file_path.name, line_number))
                            print(format_po(msgid=text_block.rstrip("\n")))


if __name__ == "__main__":
    typer.run(main)
