from io import StringIO
from typing import List, Tuple

from df_gettext_toolkit.parse_po import escape_string, unescape_string, strip_once, load_po, save_po


def test_escape_string():
    assert escape_string("\r\n\"\\\t\r") == r"\r\n\"\\\t\r"


def test_unescape_string():
    assert unescape_string(r"\r\n\"\\\t\r") == "\r\n\"\\\t\r"


def test_escape_unescape():
    s = "\r\n\"\\\t\r"
    assert unescape_string(escape_string(s)) == s


def test_strip_once():
    assert strip_once('"""', '"') == '"'


def test_load_po():
    entries: List[Tuple[str, str]] = [
        ('asddf', 'qwert'),
        ('xcvf', 'fghrth'),
        ('cvbeb', 'jtyjkty')
    ]
    template = (item[0] for item in entries)
    file = StringIO()
    save_po(file, template, dict(entries))
    file.seek(0)

    result = list(load_po(file))[1:]  # the first entry is metadata
    assert result == [dict(msgid=text, msgstr=translation) for text, translation in entries]
