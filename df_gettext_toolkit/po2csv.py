#! python3
import sys
import argparse
import csv
from collections import OrderedDict

from .po import load_po, escape_string


def cleanup_special_symbols(s):
    # TODO: Make this mapping customizable
    return s.translate({0xfeff: None, 0x2019: "'", 0x201d: '"', 0x2014: '-', 0x200b: None})


print(sys.argv, file=sys.stderr)
parser = argparse.ArgumentParser(add_help=True, description='A convertor from PO gettext format to a delimiter-separated values file')
parser.add_argument('inputfile', help='Source PO file name')
parser.add_argument('outputfile', help='A name of the output file')
parser.add_argument('codepage', help='Encoding of the outfile (cp427, cp850, cp860, cp1251 etc.)', default='utf8')

args = parser.parse_args(sys.argv[1:])

with open(args.inputfile, 'r', encoding='utf8') as pofile:
    dictionary = OrderedDict((item['msgid'], item['msgstr']) for item in load_po(pofile) if item['msgid'])

exclusions_left = {'  Choose Name  ', '  Trade Agreement with '}
exclusions_right = {'  Choose Name  '}

with open(args.outputfile, 'w', newline='', encoding=args.codepage, errors='replace') as outfile:
    writer = csv.writer(outfile, dialect='unix')
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
            
            translation = cleanup_special_symbols(translation)
            
            writer.writerow([escape_string(original_string), escape_string(translation)])
