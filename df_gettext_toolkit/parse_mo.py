from io import BytesIO
from typing import List, Iterator, Sequence, NamedTuple

from df_gettext_toolkit import TranslationItem

MO_MAGIC = b"\xde\x12\x04\x95"


def read_uint(file_object):
    return int.from_bytes(file_object.read(4), byteorder="little")


def load_string(file_object, offset) -> bytes:
    file_object.seek(offset)
    string_size = read_uint(file_object)
    string_offset = read_uint(file_object)
    file_object.seek(string_offset)
    return file_object.read(string_size)


def load_mo(mo_file, encoding="utf-8") -> Iterator[TranslationItem]:
    mo_file.seek(0)
    magic_number = mo_file.read(4)
    if magic_number != MO_MAGIC:
        raise ValueError("Wrong mo-file format")

    mo_file.seek(8)
    number_of_strings = read_uint(mo_file)
    original_string_table_offset = read_uint(mo_file)
    translation_string_table_offset = read_uint(mo_file)
    for i in range(number_of_strings):
        context, _, original_string = load_string(mo_file, original_string_table_offset + i * 8).rpartition(b"\x04")
        translation_string = load_string(mo_file, translation_string_table_offset + i * 8)

        original_string = original_string.decode(encoding)
        translation_string = translation_string.decode(encoding)
        if context:
            context = context.decode(encoding)
            yield TranslationItem(context=context, text=original_string, translation=translation_string)
        else:
            yield TranslationItem(text=original_string, translation=translation_string)


def write_uint(file_object: BytesIO, d: int):
    file_object.write(d.to_bytes(4, "little"))


def create_mo(dictionary: Sequence[TranslationItem], encoding="utf-8") -> BytesIO:
    class OffsetSizePair(NamedTuple):
        offset: int
        size: int

    mo_file_buffer = BytesIO()
    mo_file_buffer.write(MO_MAGIC)

    mo_file_buffer.seek(8)
    mo_file_buffer.write(len(dictionary).to_bytes(4, "little"))

    strings_block = BytesIO()
    originals_string_table: List[OffsetSizePair] = []
    translations_string_table: List[OffsetSizePair] = []

    for item in dictionary:
        if item.context is None:
            string = item.text.encode(encoding)
        else:
            string = item.context.encode(encoding) + b"\x04" + item.text.encode(encoding)

        translation = item.translation.encode(encoding)

        originals_string_table.append(OffsetSizePair(len(strings_block.getbuffer()), len(string)))
        strings_block.write(string)

        translations_string_table.append(OffsetSizePair(len(strings_block.getbuffer()), len(translation)))
        strings_block.write(translation)

    original_string_table_offset = len(mo_file_buffer.getbuffer()) + 8
    write_uint(mo_file_buffer, original_string_table_offset)

    translations_string_table_offset = original_string_table_offset + 8 * len(originals_string_table)
    write_uint(mo_file_buffer, translations_string_table_offset)

    strings_block_start_offset = translations_string_table_offset + 8 * len(translations_string_table)

    for offset, size in originals_string_table:
        write_uint(mo_file_buffer, size)
        write_uint(mo_file_buffer, strings_block_start_offset + offset)

    for offset, size in translations_string_table:
        write_uint(mo_file_buffer, size)
        write_uint(mo_file_buffer, strings_block_start_offset + offset)

    mo_file_buffer.write(strings_block.getbuffer())

    return mo_file_buffer
