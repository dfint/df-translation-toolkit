from collections import defaultdict


def read_uint(file_object):
    return int.from_bytes(file_object.read(4), byteorder='little')


def load_mo(mofile):
    def load_string(file_object, offset):
        file_object.seek(offset)
        string_size = read_uint(file_object)
        string_offset = read_uint(file_object)
        file_object.seek(string_offset)
        return file_object.read(string_size).decode(encoding="utf-8")
    
    mofile.seek(0)
    magic_number = mofile.read(4)
    if magic_number != b'\xde\x12\x04\x95':
        raise ValueError("Wrong mo-file format")
    
    mofile.seek(8)
    number_of_strings = read_uint(mofile)
    original_string_table_offset = read_uint(mofile)
    traslation_string_table_offset = read_uint(mofile)
    for i in range(number_of_strings):
        original_string = load_string(mofile, original_string_table_offset + i * 8)
        translation_string = load_string(mofile, traslation_string_table_offset + i * 8)
        if '\x04' in original_string:
            context, original_string = original_string.split('\x04')
        else:
            context = None
        yield dict(msgctxt=context, msgid=original_string, msgstr=translation_string)


def strip_once(s, chars=' '):
    if s and s[0] in chars:
        s = s[1:]
    if s and s[-1] in chars:
        s = s[:-1]
    return s


def unescape_string(s):
    return s\
           .replace(r'\\', '\\')\
           .replace(r'\t', '\t')\
           .replace(r'\r', '\r')\
           .replace(r'\n', '\n')\
           .replace(r'\"', '\"')


def escape_string(s):
    return s\
            .replace('\\', r'\\')\
            .replace('\t', r'\t')\
            .replace('\r', r'\r')\
            .replace('\n', r'\n')\
            .replace('\"', r'\"')


def load_po(pofile):
    def split_first(s, delimiter=' '):
        try:
            i = s.index(delimiter)
            return s[:i], s[i+len(delimiter):]
        except ValueError:
            return s, ''
    
    item = defaultdict(str)
    prev = None
    for line in pofile:
        line = line.strip()
        if not line:
            if item:
                yield item
                item = defaultdict(str)
                prev = None
        elif line.startswith('#'):
            key, value = split_first(line)
            item[key] += value
            if key == '#':
                item[key] += '\n'
        elif line.startswith('"'):
            assert prev is not None
            item[prev] += unescape_string(strip_once(line, '"'))
        else:
            # msgid, msgstr, msgctxt etc.
            key, value = split_first(line)
            item[key] = unescape_string(strip_once(value, '"'))
            prev = key
    
    yield item


def get_metadata(entry):
    def get_metadata_str(s):
        return dict(item.split(': ', maxsplit=1) for item in s.splitlines())
    
    if isinstance(entry, str):
        return get_metadata_str(entry)
    elif isinstance(entry, dict) and 'msgstr' in entry:
        return get_metadata_str(entry['msgstr'])


def format_lines(s):
    return '\n'.join('"%s"' % escape_string(x) for x in s.splitlines(keepends=True)) or '""'


def format_po(msgid, msgstr="", msgctxt=None):
    s = ""
    if msgctxt:
        s += 'msgctxt %s\n' % format_lines(msgctxt)
    s += 'msgid %s\n' % format_lines(msgid)
    s += 'msgstr %s\n' % format_lines(msgstr)
    return s


def save_po(pofile, template, dictionary):
    print('msgid ""', file=pofile)
    print('msgstr ""', file=pofile)
    print('"Content-Type: text/plain; charset=UTF-8\\n"', file=pofile)
    print('"Language: ru_RU\\n"', file=pofile)
    for text in template:
        print('', file=pofile)
        if text in dictionary and len(dictionary[text]) > 1:
            for item in dictionary[text][1:]:
                if len(item.strip()) > 0:
                    print('#', item.strip(), file=pofile)  # translator comments
        print('msgid "%s"' % escape_string(text), file=pofile)
        if text in dictionary:
            print('msgstr "%s"' % escape_string(dictionary[text][0]), file=pofile)
        else:
            print('msgstr ""', file=pofile)


def save_pot(pofile, template):
    print('msgid ""', file=pofile)
    print('msgstr ""', file=pofile)
    print('"Content-Type: text/plain; charset=UTF-8\\n"', file=pofile)
    for line in template:
        print('', file=pofile)
        print('msgid "%s"' % escape_string(line), file=pofile)
        print('msgstr ""', file=pofile)
