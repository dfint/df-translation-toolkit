import sys
from collections import defaultdict, Counter

from df_gettext_toolkit import read_uint


def load_mo(mo_file, encoding='utf-8'):
    def load_string(file_object, offset):
        file_object.seek(offset)
        string_size = read_uint(file_object)
        string_offset = read_uint(file_object)
        file_object.seek(string_offset)
        return file_object.read(string_size).decode(encoding)

    mo_file.seek(0)
    magic_number = mo_file.read(4)
    if magic_number != b'\xde\x12\x04\x95':
        raise ValueError("Wrong mo-file format")

    mo_file.seek(8)
    number_of_strings = read_uint(mo_file)
    original_string_table_offset = read_uint(mo_file)
    translation_string_table_offset = read_uint(mo_file)
    for i in range(number_of_strings):
        original_string = load_string(mo_file, original_string_table_offset + i * 8)
        translation_string = load_string(mo_file, translation_string_table_offset + i * 8)
        if '\x04' in original_string:
            context, original_string = original_string.split('\x04')
        else:
            context = None
        yield dict(msgctxt=context, msgid=original_string, msgstr=translation_string)


def show_mo_content(filename: str):
    trans = defaultdict(Counter)

    if len(sys.argv) > 1:
        with open(filename, 'rb') as mo_file:
            for item in load_mo(mo_file):
                if item['msgid']:
                    trans[item['msgid']][item['msgstr']] += 1

        for key in sorted(trans, key=lambda x: -(len(trans[x])*1000+sum(trans[x].values()))):
            print('msgid: ', key)
            print('msgstrs: ', end='')
            print(trans[key])
            print()


if __name__ == '__main__':
    show_mo_content(sys.argv[1])
