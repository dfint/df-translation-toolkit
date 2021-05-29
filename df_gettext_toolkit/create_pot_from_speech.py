import os
import sys

import typer

from .parse_po import format_po


def main(path: str = '.'):
    print('Path:', path, file=sys.stderr)

    for filename in sorted(os.listdir(path)):
        print('File:', filename, file=sys.stderr)
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path) and os.path.splitext(filename)[1] == '.txt':
            with open(full_path) as file:
                for i, line in enumerate(file, 1):
                    if line.rstrip('\n'):
                        print('#: %s:%d' % (filename, i))
                        print(format_po(msgid=line.rstrip('\n')))


if __name__ == '__main__':
    typer.run(main)
