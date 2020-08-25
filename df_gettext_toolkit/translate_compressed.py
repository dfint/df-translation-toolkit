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

            with open(backup_file, 'rb') as src:
                with open(file, 'wb') as dest:
                    yield file.name
