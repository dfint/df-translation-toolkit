#! python3
import os
import sys
import dfgettext

if len(sys.argv)>1:
    path = sys.argv[1]
else:
    path = '.'

print('Path:', path, file=sys.stderr)

for filename in os.listdir(path):
    print('File:', filename, file=sys.stderr)
    full_path = os.path.join(path, filename)
    if os.path.isfile(full_path) and os.path.splitext(filename)[1]=='.txt':
        with open(full_path) as file:
            for i, line in enumerate(file):
                if line.rstrip('\n'):
                    print('#: %s:%d' % (filename, i))
                    print(dfgettext.format_po(msgid=line.rstrip('\n')))
        