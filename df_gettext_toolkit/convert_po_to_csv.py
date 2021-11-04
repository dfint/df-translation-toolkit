#! python3
import csv
from collections import OrderedDict

import typer

from .fix_translated_strings import cleanup_string, fix_spaces
from .parse_po import load_po, escape_string


def main(input_file: str, output_file: str, encoding: str = 'utf-8'):
    with open(input_file, 'r', encoding='utf-8') as pofile:
        dictionary = OrderedDict((item['msgid'], item['msgstr']) for item in load_po(pofile) if item['msgid'])

    exclusions_leading = {'  Choose Name  ', '  Trade Agreement with '}
    exclusions_trailing = {'  Choose Name  '}

    with open(output_file, 'w', newline='', encoding=encoding, errors='replace') as outfile:
        writer = csv.writer(outfile, dialect='unix')
        if encoding == 'cp1251':
            exclusions_trailing.add('Histories of ')

        for original_string in dictionary:
            translation = dictionary[original_string]
            if original_string and translation and translation != original_string:
                translation = fix_spaces(original_string, translation, exclusions_leading, exclusions_trailing)
                writer.writerow([escape_string(original_string), escape_string(cleanup_string(translation))])


if __name__ == '__main__':
    typer.run(main)
