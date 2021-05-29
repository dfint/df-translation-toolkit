from io import StringIO

from df_gettext_toolkit.po import escape_string, unescape_string, strip_once, format_po, load_po


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
    entries = [
        ('asddf', 'qwert'),
        ('xcvf', 'fghrth'),
        ('cvbeb', 'jtyjkty')
    ]
    prepared = [dict(msgid=text, msgstr=translation) for text, translation in entries]
    po_text = '\n\n'.join(format_po(**item) for item in prepared)
    file = StringIO(po_text)
    assert list(load_po(file)) == prepared
