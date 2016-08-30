import sys
from dfgettext import *

with open(sys.argv[1]) as stringdump:
    template = (line.rstrip('\n') for line in stringdump)
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as ignored:
            ignorelist = {line.rstrip('\n').strip('|') for line in ignored}
    else:
        ignorelist = set()
    with open('DwarfFortress.pot', 'w', encoding='utf-8') as potfile:
        save_pot(potfile, (line for line in template if line not in ignorelist))
