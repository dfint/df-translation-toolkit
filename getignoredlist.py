from dfgettext import *

string_dump = LoadStringDump('stringdump_0_40_11.txt')

trans = LoadFromTrans('trans.txt')

ignored = []
for item in string_dump:
    if item[1] not in trans:
        ignored.append(item[1])
    
for item in sorted(ignored):
    print('|%s|' % item)
