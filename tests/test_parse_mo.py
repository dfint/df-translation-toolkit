from io import BytesIO
from typing import Mapping, List, Tuple

from df_gettext_toolkit.parse_mo import load_mo, MO_MAGIC


def write_uint(file_object: BytesIO, d: int):
    file_object.write(d.to_bytes(4, 'little'))


def create_mo(dictionary: Mapping[str, str]) -> BytesIO:
    mo_file = BytesIO()
    mo_file.write(MO_MAGIC)

    mo_file.seek(8)
    mo_file.write(len(dictionary).to_bytes(4, 'little'))

    strings_block = BytesIO()
    originals_string_table: List[Tuple[int, int]] = []
    translations_string_table: List[Tuple[int, int]] = []

    for string, translation in dictionary.items():
        originals_string_table.append((len(strings_block.getbuffer()), len(string)))
        strings_block.write(string.encode('utf-8'))
        translations_string_table.append((len(strings_block.getbuffer()), len(translation)))
        strings_block.write(translation.encode('utf-8'))

    original_string_table_offset = len(mo_file.getbuffer()) + 8
    translations_string_table_offset = original_string_table_offset + 8 * len(originals_string_table)
    write_uint(mo_file, original_string_table_offset)
    write_uint(mo_file, translations_string_table_offset)

    strings_block_start_offset = translations_string_table_offset + 8 * len(translations_string_table)

    for offset, size in originals_string_table:
        write_uint(mo_file, size)
        write_uint(mo_file, strings_block_start_offset + offset)

    for offset, size in translations_string_table:
        write_uint(mo_file, size)
        write_uint(mo_file, strings_block_start_offset + offset)

    mo_file.write(strings_block.getbuffer())

    return mo_file


def test_load_mo():
    d = {
        "Word1": "Translation1",
        "Word2": "Translation2",
        "LongWord": "LongTranslation"
    }
    mo_file = create_mo(d)
    assert {item['msgid']: item['msgstr'] for item in load_mo(mo_file)} == d
