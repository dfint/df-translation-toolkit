from dfgettext import *

template = LoadStringDump('stringdump_0_40_12.txt')
ignorelist = {line[1] for line in LoadDSV('ignored.txt')}
# dictionary = LoadFromTrans('trans.txt')
SavePOT('DwarfFortress.pot',template,ignorelist)
