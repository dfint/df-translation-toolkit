from dfgettext import *

with open(sys.argv[1]) as stringdump:
    template = load_string_dump(stringdump)
    with open('ignored.txt') as ignored:
        ignorelist = {line[1] for line in load_dsv(ignored)}
    
    with open('trans.txt') as trans:
        dictionary = load_trans(trans)
    
    with open('DwarfFortress.po', 'w', encoding='cp65001') as pofile:
        save_po(pofile, template, dictionary, ignorelist)
