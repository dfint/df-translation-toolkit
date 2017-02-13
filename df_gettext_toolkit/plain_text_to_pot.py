#! python3

import os
import sys
from .parse_raws import  parse_plain_text_file
from .po import format_po

def skip_tags(s):
    opened = 0
    for char in s:
        if char == '[':
            opened += 1
        elif char == ']':
            opened -= 1
        elif opened == 0:
            yield char


def parse_file(file, join_paragraphs=True):
    first_line = file.readline()
    prev_lines = ''
    for line in file:
        if any(char.islower() for char in skip_tags(line)):
            if not join_paragraphs or '~' in line or line[0] == '[' and not (prev_lines and prev_lines.rstrip()[-1].isalpha()):
                if prev_lines:
                    yield prev_lines
                    prev_lines = ''
                    
                if line.endswith(']\n') or line[-1] == ']':
                    yield line
                else:
                    prev_lines += line
            else:
                prev_lines += line
        elif prev_lines:
            yield prev_lines
            prev_lines = ''
    if prev_lines:
        yield prev_lines

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = '.'

join_paragraphs = '--split' not in sys.argv[1:]

keys = set()
for cur_dir, _, files in os.walk(path):
    for file_name in files:
        full_path = os.path.join(cur_dir, file_name)
        if os.path.isfile(full_path) and os.path.splitext(file_name)[1]=='.txt':
            print(full_path, file=sys.stderr)
            with open(full_path) as file:
                for text_block, is_translatable in parse_plain_text_file(file, join_paragraphs):
                    if not is_translatable:
                        pass
                    elif text_block in keys:
                        print('Key already exists:', repr(text_block), file=sys.stderr)
                    else:
                        keys.add(text_block)
                        print('#: %s' % file_name)
                        print(format_po(msgid=text_block.rstrip('\n')))
