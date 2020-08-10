import sys

from pathlib import Path

import click

from .translate_raws import translate_raws
from .translate_plain_text import translate_plain_text


@click.command()
@click.argument('base_path')
@click.argument('po_directory')
@click.option('--encoding', default='cp1251')
@click.option('--po_name_prefix', default='')
@click.option('--po_name_postfix', default='')
def main(base_path, po_directory, encoding, po_name_prefix, po_name_postfix):
    patterns = {
        'raw/objects': dict(
            po_filename='raw-objects.po',
            func=translate_raws,
        ),
        'data_src': dict(
            po_filename='uncompressed.po',
            func=lambda *args: translate_plain_text(*args, join_paragraphs=True),
        ),
        'data/speech': dict(
            po_filename='speech.po',
            func=lambda *args: translate_plain_text(*args, join_paragraphs=False),
        ),
        'raw/objects/text': dict(
            po_filename='text.po',
            func=lambda *args: translate_plain_text(*args, join_paragraphs=False),
        ),
    }

    po_directory = Path(po_directory)

    for cur_dir in Path(base_path).rglob("*"):
        if cur_dir.is_dir():
            for pattern in patterns:
                if cur_dir.match('*/' + pattern):
                    print(f"Matched {pattern} pattern")
                    print(cur_dir, file=sys.stderr)
                    print(file=sys.stderr)

                    po_filename = po_name_prefix + patterns[pattern]['po_filename']
                    if po_name_postfix:
                        name, sep, ext = po_filename.partition('.')
                        po_filename = name + po_name_postfix + sep + ext

                    po_file_path = po_directory / po_filename
                    func = patterns[pattern]['func']
                    for filename in func(po_file_path, cur_dir, encoding):
                        print(filename, file=sys.stderr)
                    print(file=sys.stderr)


if __name__ == '__main__':
    main()
