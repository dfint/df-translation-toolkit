import sys

from pathlib import Path

import click

from .translate_raws import translate_raws
from .translate_plain_text import translate_plain_text


@click.command()
@click.argument('base_path')
@click.argument('po_file_path')
@click.option('--encoding', default='cp1251')
@click.option('--prefix', default='')
def main(base_path, po_file_path, encoding, prefix):
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

    po_file_path = Path(po_file_path)

    for cur_dir in Path(base_path).rglob("*"):
        if cur_dir.is_dir():
            for pattern in patterns:
                if cur_dir.match('*/' + pattern):
                    print(f"Matched {pattern} pattern")
                    print(cur_dir, file=sys.stderr)
                    print(file=sys.stderr)
                    po_filename = po_file_path / (prefix + patterns[pattern]['po_filename'])
                    func = patterns[pattern]['func']
                    for filename in func(po_filename, cur_dir, encoding):
                        print(filename, file=sys.stderr)
                    print(file=sys.stderr)


if __name__ == '__main__':
    main()
