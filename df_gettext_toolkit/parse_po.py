from collections import defaultdict
from typing import Mapping, Iterator


def strip_once(s, chars=" "):
    if s and s[0] in chars:
        s = s[1:]
    if s and s[-1] in chars:
        s = s[:-1]
    return s


_replace_table = [
    ("\\", r"\\"),
    ("\t", r"\t"),
    ("\r", r"\r"),
    ("\n", r"\n"),
    ('"', r"\""),
]

_unescape_translation_table = {escaped: unescaped for unescaped, escaped in _replace_table}


def unescape_string(s):
    for original, replacement in _unescape_translation_table.items():
        s = s.replace(original, replacement)
    return s


_escape_translation_table = str.maketrans(dict(_replace_table))


def escape_string(s):
    return s.translate(_escape_translation_table)


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
        elif line.startswith("#"):
            key, _, value = line.partition(" ")
            item[key] += value
            if key == "#":
                item[key] += "\n"
        elif line.startswith('"'):
            assert prev is not None
            item[prev] += unescape_string(strip_once(line, '"'))
        else:
            # msgid, msgstr, msgctxt etc.
            key, value = line.split(maxsplit=1)
            item[key] = unescape_string(strip_once(value, '"'))
            prev = key

    if item:
        yield item


def get_metadata(entry) -> Mapping[str, str]:
    def get_metadata_str(s):
        return dict(item.split(": ", maxsplit=1) for item in s.splitlines())

    if isinstance(entry, str):
        return get_metadata_str(entry)
    elif isinstance(entry, dict) and "msgstr" in entry:
        return get_metadata_str(entry["msgstr"])


class PoReader:
    def __init__(self, file_object):
        file_object.seek(0)
        self._iterator = load_po(file_object)
        first_entry = next(self._iterator)
        assert first_entry["msgid"] == "", "No metadata entry in the po file"
        self.meta = get_metadata(first_entry)

    def __iter__(self):
        return self._iterator


def format_lines(line: str):
    return "\n".join(f'"{escape_string(x)}"' for x in line.splitlines(keepends=True)) or '""'


def format_po_item(msgid: str, msgstr: str = "", msgctxt: str = None, file_name: str = None, line_number: int = None):
    lines = list()
    if file_name:
        lines.append(f"#: {file_name}:{line_number:d}")

    if msgctxt:
        lines.append(f"msgctxt {format_lines(msgctxt)}")

    lines.append(f"msgid {format_lines(msgid)}")
    lines.append(f"msgstr {format_lines(msgstr)}")
    return "\n".join(lines)


default_header = """
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
""".strip()


def save_po(po_file, template: Iterator[str], dictionary: Mapping[str, str]):
    print(default_header, file=po_file)
    print(file=po_file)
    for text in template:
        print(format_po_item(msgid=text, msgstr=dictionary.get(text, "")), file=po_file, end="\n\n")


def save_pot(po_file, template):
    print(default_header, file=po_file, end="\n\n")
    for line in template:
        print(format_po_item(msgid=line), file=po_file, end="\n\n")
