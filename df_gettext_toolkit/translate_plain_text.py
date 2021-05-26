import sys

from pathlib import Path
from typing import Optional

import typer

from .parse_raws import parse_plain_text_file
from .po import load_po
from .backup import backup


def translate_plain_text(po_filename, path, encoding, join_paragraphs=True):
    with open(po_filename, 'r', encoding='utf-8') as pofile:
        dictionary = {item['msgid']: item['msgstr'] for item in load_po(pofile)}

    for path in Path(path).rglob("*.txt"):
        if path.is_file():
            with backup(path) as backup_file:
                with open(backup_file) as src:
                    with open(path, 'w', encoding=encoding) as dest:
                        yield path.name
                        for text_block, is_translatable, _ in parse_plain_text_file(src, join_paragraphs):
                            text_block = text_block.rstrip('\n')
                            if text_block in dictionary:
                                translation = dictionary[text_block]
                                if not translation:
                                    translation = text_block
                            else:
                                translation = text_block
                            print(translation, file=dest)


def main(po_filename: str, path: str = '.', encoding: Optional[str] = None, split: bool = False):
    join_paragraphs = not split
    for filename in translate_plain_text(po_filename, path, encoding, join_paragraphs):
        print(filename, file=sys.stderr)


if __name__ == "__main__":
    typer.run(main)
