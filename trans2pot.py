﻿import sys
from dfgettext import *

with open(sys.argv[1]) as stringdump:
    template = load_string_dump(stringdump)
    if len(sys.argv) > 1:
        with open(sys.argv[2]) as ignored:
            ignorelist = {line[1] for line in load_dsv(ignored)}
    else:
        ignorelist = set()
    
    with open('DwarfFortress.pot', 'w', encoding='utf-8') as potfile:
        save_pot(potfile, template, ignorelist)
