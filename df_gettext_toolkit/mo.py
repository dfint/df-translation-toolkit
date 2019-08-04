from df_gettext_toolkit import read_uint


def load_mo(mofile, encoding='utf-8'):
    def load_string(file_object, offset):
        file_object.seek(offset)
        string_size = read_uint(file_object)
        string_offset = read_uint(file_object)
        file_object.seek(string_offset)
        return file_object.read(string_size).decode(encoding)

    mofile.seek(0)
    magic_number = mofile.read(4)
    if magic_number != b'\xde\x12\x04\x95':
        raise ValueError("Wrong mo-file format")

    mofile.seek(8)
    number_of_strings = read_uint(mofile)
    original_string_table_offset = read_uint(mofile)
    translation_string_table_offset = read_uint(mofile)
    for i in range(number_of_strings):
        original_string = load_string(mofile, original_string_table_offset + i * 8)
        translation_string = load_string(mofile, translation_string_table_offset + i * 8)
        if '\x04' in original_string:
            context, original_string = original_string.split('\x04')
        else:
            context = None
        yield dict(msgctxt=context, msgid=original_string, msgstr=translation_string)