import sys

from dfgettext import *

with open(sys.argv[1], 'rb') as mofile:
    dictionary = {item['msgid']:item['msgstr'] for item in LoadMO(mofile)}

with open(sys.argv[2]) as stringdump:
    template = LoadStringDump(stringdump)

    exclusions = {'Histories of '}

    for id, original_string in template:
        if original_string in dictionary:
            translation = dictionary[original_string]
            if translation != original_string:
                if original_string not in exclusions:
                    if original_string[0]==' ' and translation[0]!=' ' and translation[0]!=',':
                        translation = ' '+translation
                        print("Warning: leading space added for the translation of the '%s' string." % original_string, file = sys.stderr)
                    if original_string[-1]==' ' and translation[-1]!=' ':
                        translation = translation+' '
                        print("Warning: trailing space added for the translation of the '%s' string." % original_string, file = sys.stderr)
                print("%s|%s|%s|" % (id, original_string, translation))
