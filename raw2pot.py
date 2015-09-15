import sys
import os

from dfgettext import *

if len(sys.argv)<2:
    path = '.'
else:
    path = sys.argv[1]

raws = filter(lambda x: not x.startswith('language_'), os.listdir(path))

potfilename = sys.argv[2]
with open(potfilename, 'w', encoding='utf-8') as potfile:
    for file_name in raws:
        fullpath = os.path.join(path, file_name)
        if os.path.isfile(fullpath) and file_name.endswith('.txt'):
            with open(fullpath) as file:
                for context, item in extract_translatables_from_raws(file):
                    print('#:', file_name, file=potfile)
                    print(format_po(msgid=item, msgstr="", msgctxt=context), file=potfile)
