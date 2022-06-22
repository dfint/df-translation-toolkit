from io import BytesIO
from typing import List, Mapping, Tuple
import typer

from .parse_po import format_po

MO_MAGIC = b'\xde\x12\x04\x95'


def read_uint(file_object):
    return int.from_bytes(file_object.read(4), byteorder='little')


def load_string(file_object, offset) -> bytes:
    file_object.seek(offset)
    string_size = read_uint(file_object)
    string_offset = read_uint(file_object)
    file_object.seek(string_offset)
    return file_object.read(string_size)


def load_mo(mo_file, encoding='utf-8'):
    mo_file.seek(0)
    magic_number = mo_file.read(4)
    if magic_number != MO_MAGIC:
        raise ValueError("Wrong mo-file format")

    mo_file.seek(8)
    number_of_strings = read_uint(mo_file)
    original_string_table_offset = read_uint(mo_file)
    translation_string_table_offset = read_uint(mo_file)
    for i in range(number_of_strings):
        original_string = load_string(mo_file, original_string_table_offset + i * 8).decode(encoding)
        translation_string = load_string(mo_file, translation_string_table_offset + i * 8).decode(encoding)

        context, _, original_string = original_string.rpartition('\x04')
        if context:
            yield dict(msgctxt=context, msgid=original_string, msgstr=translation_string)
        else:
            yield dict(msgid=original_string, msgstr=translation_string)


def show_mo_content(filename: str):
    with open(filename, 'rb') as mo_file:
        for item in load_mo(mo_file):
            print(format_po(**item), end='\n\n')


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


if __name__ == '__main__':
    typer.run(show_mo_content)
