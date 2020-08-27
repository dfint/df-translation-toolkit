import shutil

from pathlib import Path

from .parse_raws import parse_plain_text_file
from .po import load_po

from df_raw_decoder import decode_data


def translate_compressed(po_filename, path, encoding):
    with open(po_filename, 'r', encoding='utf-8') as pofile:
        dictionary = {item['msgid']: item['msgstr'] for item in load_po(pofile)}

    for file in Path(path).rglob('*'):
        if file.is_file() and file.suffix == '':
            backup_file = file.with_suffix('.bak')
            if not backup_file.exists():
                shutil.copy(file, backup_file)

            is_index_file = file.name == 'index'

            with open(backup_file, 'rb') as src:
                with open(file, 'w', encoding=encoding) as dest:
                    yield file.name

                    lines = (line.decode('cp437') for line in decode_data(src, is_index_file))
                    for text_block, is_translatable, _ in parse_plain_text_file(lines, True):
                        if text_block in dictionary:
                            translation = dictionary[text_block]
                            if not translation:
                                translation = text_block
                        else:
                            translation = text_block
                        print(translation, file=dest)
