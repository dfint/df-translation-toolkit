import sys
from dfgettext import *

with open(sys.argv[1]) as stringdump:
    template = load_string_dump(stringdump)
    with open('ignored.txt') as ignored:
        ignorelist = {line[1] for line in load_dsv(ignored)}
    
    with open('DwarfFortress.pot', 'w', encoding='cp65001') as potfile:
        save_pot(potfile, template, ignorelist)
