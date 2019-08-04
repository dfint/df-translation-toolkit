import click
import os
import sys

from .parse_raws import extract_translatables_from_raws
from .po import format_po


@click.command()
@click.argument('pot_filename')
@click.argument('path', default='.')
@click.argument('source_encoding', default='cp437')
def main(pot_filename, path, source_encoding):
    raw_files = filter(lambda x: not x.startswith('language_'), os.listdir(path))

    with open(pot_filename, 'w', encoding='utf-8') as potfile:
        for file_name in raw_files:
            print(file_name, file=sys.stderr)
            full_path = os.path.join(path, file_name)
            if os.path.isfile(full_path) and file_name.endswith('.txt'):
                with open(full_path, encoding=source_encoding) as file:
                    for context, item, line_number in extract_translatables_from_raws(file):
                        print('#: %s:%d' % (file_name, line_number), file=potfile)  # source file : line number
                        print(format_po(msgid=item, msgstr="", msgctxt=context), file=potfile)


if __name__ == '__main__':
    main()
