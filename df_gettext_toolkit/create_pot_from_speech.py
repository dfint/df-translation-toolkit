import os
import sys
from .po import format_po


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '.'

    print('Path:', path, file=sys.stderr)

    for filename in sorted(os.listdir(path)):
        print('File:', filename, file=sys.stderr)
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path) and os.path.splitext(filename)[1] == '.txt':
            with open(full_path) as file:
                for i, line in enumerate(file):
                    if line.rstrip('\n'):
                        print('#: %s:%d' % (filename, i))
                        print(format_po(msgid=line.rstrip('\n')))
