from pathlib import Path

from .backup import backup
from .parse_raws import parse_plain_text_file
from .parse_po import load_po

from df_raw_decoder import decode_data
from df_raw_decoder import encode_data


def translate_compressed(po_filename, path, encoding):
    with open(po_filename, 'r', encoding='utf-8') as pofile:
        dictionary = {item['msgid']: item['msgstr'] for item in load_po(pofile)}

    for file in Path(path).rglob('*'):
        if file.is_file() and file.suffix == '':
            is_index_file = file.name == 'index'
            # Fix crash game due to changes in index file
            if is_index_file:
                continue

            with backup(file) as backup_file:
                with open(backup_file, 'rb') as src:
                    with open(file, 'wb') as dest:
                        yield file.name

                        translations = []

                        lines = (line.decode('cp437') for line in decode_data(src, is_index_file))
                        for text_block, is_translatable, _ in parse_plain_text_file(lines, True):
                            if text_block in dictionary:
                                translation = dictionary[text_block]
                                if not translation:
                                    translation = text_block
                            else:
                                translation = text_block
                            translations.append(translation.encode(encoding))

                        dest.write(encode_data(translations, is_index_file))
