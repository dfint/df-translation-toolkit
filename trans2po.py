from dfgettext import *

with open(sys.argv[1]) as stringdump:
    template = LoadStringDump(stringdump)
    with open('ignored.txt') as ignored:
        ignorelist = {line[1] for line in LoadDSV(ignored)}
    
    with open('trans.txt') as trans:
        dictionary = LoadFromTrans(trans)
    
    with open('DwarfFortress.po', 'w', encoding='cp65001') as pofile:
        SavePO(pofile, template, dictionary, ignorelist)
