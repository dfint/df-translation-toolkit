from dfgettext import *

with open(sys.argv[1]) as stringdump:
    template = (line.rstrip('\n') for line in stringdump)
    with open('ignored.txt') as ignored:
        ignorelist = {line[1] for line in load_dsv(ignored)}
    
    with open('trans.txt') as trans:
        dictionary = load_trans(trans)
    
    with open('DwarfFortress.po', 'w', encoding='cp65001') as pofile:
        save_po(pofile, (line for line in template if line not in ignorelist), dictionary)
