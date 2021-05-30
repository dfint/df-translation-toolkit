import os
import sys
from operator import itemgetter

import typer

from .parse_plain_text import parse_plain_text_file
from .parse_po import format_po


def main(path: str = '.', split: bool = False):
    join_paragraphs = not split

    keys = set()
    for cur_dir, _, files in sorted(os.walk(path), key=itemgetter(0)):
        for file_name in sorted(files):
            full_path = os.path.join(cur_dir, file_name)
            if os.path.isfile(full_path) and os.path.splitext(file_name)[1] == '.txt':
                print(full_path, file=sys.stderr)
                with open(full_path) as file:
                    for text_block, is_translatable, line_number in parse_plain_text_file(file, join_paragraphs):
                        if not is_translatable:
                            pass
                        elif text_block in keys:
                            print('Key already exists:', repr(text_block), file=sys.stderr)
                        else:
                            keys.add(text_block)
                            print('#: %s:%d' % (file_name, line_number))
                            print(format_po(msgid=text_block.rstrip('\n')))


if __name__ == '__main__':
    typer.run(main)
