#! python3

import os
import sys
import dfgettext


def skip_tags(s):
    opened = 0
    for char in s:
        if char == '[':
            opened += 1
        elif char == ']':
            opened -= 1
        elif opened == 0:
            yield char


def parse_file(file):
    first_line = file.readline()
    prev_lines = ''
    for line in file:
        if any(char.islower() for char in skip_tags(line)):
            if line[0] == '[' or '~' in line:
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

keys = set()
for cur_dir, _, files in os.walk(path):
    for file_name in files:
        full_path = os.path.join(cur_dir, file_name)
        if os.path.isfile(full_path) and os.path.splitext(file_name)[1]=='.txt':
            print(full_path, file=sys.stderr)
            with open(full_path) as file:
                for parsed_line in parse_file(file):
                    if parsed_line in keys:
                        print('Key already exists:', repr(parsed_line), file=sys.stderr)
                    else:
                        keys.add(parsed_line)
                        print('#: %s' % file_name)
                        print(dfgettext.format_po(msgid=parsed_line.rstrip('\n')))
