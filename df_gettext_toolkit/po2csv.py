#! python3
import sys
import csv
from collections import OrderedDict

import typer

from .po import load_po, escape_string
from .fix_translated_strings import cleanup_string


def main(input_file: str, output_file: str, encoding: str = 'utf-8'):
    with open(input_file, 'r', encoding='utf-8') as pofile:
        dictionary = OrderedDict((item['msgid'], item['msgstr']) for item in load_po(pofile) if item['msgid'])

    exclusions_left = {'  Choose Name  ', '  Trade Agreement with '}
    exclusions_right = {'  Choose Name  '}

    with open(output_file, 'w', newline='', encoding=encoding, errors='replace') as outfile:
        writer = csv.writer(outfile, dialect='unix')
        if encoding == 'cp1251':
            exclusions_right.add('Histories of ')

        for original_string in dictionary:
            translation = dictionary[original_string]
            if original_string and translation and translation != original_string:
                if (original_string not in exclusions_left and
                        original_string[0] == ' ' and
                        translation[0] != ' ' and
                        translation[0] != ','):
                    translation = ' ' + translation
                    print("Leading space added to the translation of the string: %r" % original_string, file=sys.stderr)

                if original_string not in exclusions_right and original_string[-1] == ' ' and translation[-1] != ' ':
                    translation += ' '
                    print("Trailing space added to the translation of the string: %r" % original_string, file=sys.stderr)

                translation = cleanup_string(translation)

                writer.writerow([escape_string(original_string), escape_string(translation)])


if __name__ == '__main__':
    typer.run(main)
