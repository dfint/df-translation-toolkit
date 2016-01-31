#! python3

import os
import sys
import dfgettext
from dfgettext import parse_plain_text_file

pofilename = sys.argv[1]
with open(pofilename, 'r', encoding='utf-8') as pofile:
    dictionary = {item['msgid']: item['msgstr'] for item in load_po(pofile)}

if len(sys.argv) > 2:
    path = sys.argv[2]
else:
    path = '.'

files = os.listdir(path)

join_paragraphs = '--split' not in sys.argv[1:]

for file_name in files:
    basename, ext = os.path.splitext(file_name)
    if ext == '.txt':
        bak_name = os.path.join(path, basename+'.bak')
        dest_name = os.path.join(path, file_name)
        
        if not os.path.exists(bak_name):
            shutil.copy(dest_name, bak_name)
        
        with open(bak_name) as src:
            with open(dest_name, 'w', encoding='cp1251') as dest:
                print(dest_name, file=sys.stderr)
                for text_block, is_translatable in parse_plain_text_file(src):
                    text_block = text_block.rstrip('\n')
                    if is_translatable:
                        print(dictionary.get(text_block, text_block), file=dest)
                    else:
                        print(text_block, file=dest)