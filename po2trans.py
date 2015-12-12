#! python3
import sys
import argparse
from collections import OrderedDict

from dfgettext import *

print(sys.argv, file=sys.stderr)
parser = argparse.ArgumentParser(add_help=True, description='A convertor from MO gettext format to a delimiter-separated values file')
parser.add_argument('inputfile', help='Source PO file name')
parser.add_argument('outputfile', help='A name of the output file')
parser.add_argument('codepage', help='Encoding of the outfile (cp427, cp850, cp860, cp1251 etc.)')

args = parser.parse_args(sys.argv[1:])

with open(args.inputfile, 'r', encoding='utf8') as pofile:
    dictionary = OrderedDict((item['msgid'], item['msgstr']) for item in load_po(pofile) if item['msgid'])

exclusions_left = {'  Choose Name  ', '  Trade Agreement with '}
exclusions_right = {'  Choose Name  '}

with open(args.outputfile, 'wb') as outfile:
    if args.codepage == 'cp1251':
        exclusions_right.add('Histories of ')
    
    for original_string in dictionary:
        translation = dictionary[original_string]
        if original_string and translation and translation != original_string:
            if (original_string not in exclusions_left and
                    original_string[0]==' ' and
                        translation[0]!=' ' and
                        translation[0]!=','):
                translation = ' ' + translation
                print("Leading space added to the translation of the string: %r" % original_string, file=sys.stderr)
            
            if original_string not in exclusions_right and original_string[-1]==' ' and translation[-1]!=' ':
                translation += ' '
                print("Trailing space added to the translation of the string: %r" % original_string, file=sys.stderr)
            
            translation = translation.translate({0xfeff: None, 0x2019: "'", 0x201d: '"'})
            line = "|%s|%s|\r\n" % (original_string, translation)
            # Try to encode strict:
            try:
                encoded = line.encode(args.codepage, errors='strict')
            except UnicodeEncodeError:
                print('Some characters in the translation of string %r '
                      'cannot be represented in cp%d. Using backslashreplace mode.' %
                      (original_string, args.codepage), file=sys.stderr)
                encoded = line.encode(args.codepage, errors='backslashreplace')
            outfile.write(encoded)
