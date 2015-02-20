import sys
from dfgettext import *

with open(sys.argv[1]) as stringdump:
    template = LoadStringDump(stringdump)
    with open('ignored.txt') as ignored:
        ignorelist = {line[1] for line in LoadDSV(ignored)}
    
    with open('DwarfFortress.pot', 'w', encoding='cp65001') as potfile:
        SavePOT(potfile, template, ignorelist)
