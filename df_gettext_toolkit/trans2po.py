import sys

from .parse_raws import load_trans
from .po import save_po

with open(sys.argv[1]) as stringdump:
    template = (line.rstrip('\n') for line in stringdump)
    with open('ignored.txt') as ignored:
        ignorelist = {line.rstrip('\n').strip('|') for line in ignored}
    
    with open('trans.txt') as trans:
        dictionary = load_trans(trans)
    
    with open('DwarfFortress.po', 'w', encoding='cp65001') as pofile:
        save_po(pofile, (line for line in template if line not in ignorelist), dictionary)
