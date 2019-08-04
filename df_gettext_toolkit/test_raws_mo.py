import sys

from df_gettext_toolkit.mo import load_mo

from collections import defaultdict, Counter

trans = defaultdict(Counter)

if len(sys.argv)>1:
    for item in load_mo(sys.argv[1]):
        if item['msgid']:
            trans[item['msgid']][item['msgstr']]+=1

    for key in sorted(trans, key=lambda x: -(len(trans[x])*1000+sum(trans[x].values()))):
        print('msgid: ', key)
        print('msgstrs: ', end='')
        print(trans[key])
        print()
