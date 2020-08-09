import os
import sys

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
        r'raw\objects': dict(
            po_filename='raw-objects.po',
            func=translate_raws,
        ),
        r'data_src': dict(
            po_filename='uncompressed.po',
            func=lambda *args: translate_plain_text(*args, join_paragraphs=True),
        ),
        r'data\speech': dict(
            po_filename='speech.po',
            func=lambda *args: translate_plain_text(*args, join_paragraphs=False),
        ),
        r'raw\objects\text': dict(
            po_filename='text.po',
            func=lambda *args: translate_plain_text(*args, join_paragraphs=False),
        ),
    }

    for cur_dir, _, files in os.walk(base_path):
        print(cur_dir)
        for pattern in patterns:
            if cur_dir.replace('/', '\\').endswith(pattern):
                print(f"Matched {pattern} pattern")
                print(cur_dir, file=sys.stderr)
                print(file=sys.stderr)
                po_filename = os.path.join(po_file_path, prefix+patterns[pattern]['po_filename'])
                func = patterns[pattern]['func']
                for filename in func(po_filename, cur_dir, encoding):
                    print(filename, file=sys.stderr)
                print(file=sys.stderr)
