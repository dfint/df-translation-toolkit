from df_gettext_toolkit.po import escape_string, unescape_string, strip_once


def test_escape_string():
    assert escape_string("\r\n\"\\\t\r") == r"\r\n\"\\\t\r"


def test_unescape_string():
    assert unescape_string(r"\r\n\"\\\t\r") == "\r\n\"\\\t\r"


def test_escape_unescape():
    s = "\r\n\"\\\t\r"
    assert unescape_string(escape_string(s)) == s


def test_strip_once():
    assert strip_once('"""', '"') == '"'
