from dfgettext import *

with open('trans.txt') as transfile:
    trans = LoadFromTrans(transfile)

with open('stringdump_0_40_24_noprefix.txt') as dumpfile:
    string_dump = LoadStringDump(dumpfile)
    ignored = (item[1] for item in string_dump if item[1] not in trans)
        
    for item in sorted(ignored):
        print('|%s|' % item)
