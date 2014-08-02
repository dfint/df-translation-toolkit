from dfgettext import *

strings_0_34_11 = LoadStringDump('stringdump_0_40_04.txt')

trans = LoadFromTrans('trans.txt')

ignored = []
for item in strings_0_34_11:
    if item[1] not in trans:
        ignored.append(item[1])
        
for item in sorted(ignored):
    print('|%s|' % item)
