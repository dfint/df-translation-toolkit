# What The File is this ?

import sys
from .parse_raws import split_tag, is_translatable, last_suitable, bracket_tag
from .po import load_mo, format_po

mofilename = sys.argv[1]
with open(mofilename, 'rb') as mofile:
    imported = [item for item in load_mo(mofile)]

pofilename = sys.argv[2]
with open(pofilename, 'w', encoding='utf-8') as pofile:
    print('msgid ""', file=pofile)
    print('msgstr ""', file=pofile)
    print('"Content-Type: text/plain; charset=UTF-8\\n"', file=pofile)
    
    for item in imported:
        if item['msgid']:
            msgid = split_tag(item['msgid'])
            msgstr = split_tag(item['msgstr'])
            if not is_translatable(msgid[-1]):
                last = last_suitable(msgid, is_translatable)
                msgid = msgid[:last+1]
                msgid[-1] = ''
                msgstr = msgstr[:last+1]
                msgstr[-1] = ''
                item['msgid'] = bracket_tag(msgid)
                item['msgstr'] = bracket_tag(msgstr)
            print(format_po(**item), file=pofile)
