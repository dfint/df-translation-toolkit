import sys
from dfgettext import *

dictionary = {item['msgid']:item['msgstr'] for item in LoadMO('out.mo')}
template = LoadStringDump('stringdump_0_40_24_noprefix.txt')

exclusions = {'Histories of '}

with open('tmp_trans.txt','w',encoding='cp1251') as tmp_trans:
    for id, original_string in template:
        if original_string in dictionary:
            translation = dictionary[original_string]
            if original_string not in exclusions:
                if original_string[0]==' ' and translation[0]!=' ' and translation[0]!=',':
                    translation = ' '+translation
                    print("Warning: leading space added for the translation of the '%s' string." % original_string)
                if original_string[-1]==' ' and translation[-1]!=' ':
                    translation = translation+' '
                    print("Warning: trailing space added for the translation of the '%s' string." % original_string)
            print("%s|%s|%s|" % (id, original_string, translation), file=tmp_trans)
