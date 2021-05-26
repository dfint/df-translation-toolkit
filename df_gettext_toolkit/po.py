from collections import defaultdict


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


def load_po(po_file):
    item = defaultdict(str)
    prev = None
    for line in po_file:
        line = line.strip()
        if not line:
            if item:
                yield item
                item = defaultdict(str)
                prev = None
        elif line.startswith('#'):
            key, _, value = line.partition(' ')
            item[key] += value
            if key == '#':
                item[key] += '\n'
        elif line.startswith('"'):
            assert prev is not None
            item[prev] += unescape_string(strip_once(line, '"'))
        else:
            # msgid, msgstr, msgctxt etc.
            key, value = line.split(maxsplit=1)
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


class PoReader:
    def __init__(self, file_object):
        file_object.seek(0)
        self._iterator = load_po(file_object)
        first_entry = next(self._iterator)
        assert first_entry['msgid'] == '', 'No metadata entry in the po file'
        self.meta = get_metadata(first_entry)
    
    def __iter__(self):
        return self._iterator


def format_lines(s):
    return '\n'.join('"%s"' % escape_string(x) for x in s.splitlines(keepends=True)) or '""'


def format_po(msgid, msgstr="", msgctxt=None):
    s = ""
    if msgctxt:
        s += 'msgctxt %s\n' % format_lines(msgctxt)
    s += 'msgid %s\n' % format_lines(msgid)
    s += 'msgstr %s\n' % format_lines(msgstr)
    return s


def save_po(po_file, template, dictionary):
    print('msgid ""', file=po_file)
    print('msgstr ""', file=po_file)
    print('"Content-Type: text/plain; charset=UTF-8\\n"', file=po_file)
    print('"Language: ru_RU\\n"', file=po_file)
    for text in template:
        print('', file=po_file)
        if text in dictionary and len(dictionary[text]) > 1:
            for item in dictionary[text][1:]:
                if len(item.strip()) > 0:
                    print('#', item.strip(), file=po_file)  # translator comments
        print('msgid "%s"' % escape_string(text), file=po_file)
        if text in dictionary:
            print('msgstr "%s"' % escape_string(dictionary[text][0]), file=po_file)
        else:
            print('msgstr ""', file=po_file)


default_pot_header = """
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
""".lstrip()


def save_pot(po_file, template):
    print(default_pot_header, file=po_file)
    for line in template:
        print(format_po(line), file=po_file)
