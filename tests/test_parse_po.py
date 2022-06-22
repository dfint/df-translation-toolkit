from io import StringIO
from typing import List, Tuple

from df_gettext_toolkit.parse_po import (
    escape_string,
    unescape_string,
    strip_once,
    load_po,
    save_po,
    PoReader,
)


def test_escape_string():
    assert escape_string('\r\n"\\\t\r') == r"\r\n\"\\\t\r"


def test_unescape_string():
    assert unescape_string(r"\r\n\"\\\t\r") == '\r\n"\\\t\r'


def test_escape_unescape():
    s = '\r\n"\\\t\r'
    assert unescape_string(escape_string(s)) == s


def test_strip_once():
    assert strip_once('"""', '"') == '"'


def test_load_po():
    data = """
    # Some comment
    #: body_default.txt:7
    msgctxt "BODY:BASIC_1PARTBODY"
    msgid "[BP:UB:body:bodies]"
    msgstr "[BP:UB:тело:тела]"
    """

    expected = {
        "#": "Some comment\n",
        "#:": "body_default.txt:7",
        "msgctxt": "BODY:BASIC_1PARTBODY",
        "msgid": "[BP:UB:body:bodies]",
        "msgstr": "[BP:UB:тело:тела]",
    }

    file = StringIO(data)
    result = next(load_po(file))
    assert result == expected


def test_save_load_po():
    entries: List[Tuple[str, str]] = [
        ("asddf", "qwert"),
        ("xcvf", "fghrth"),
        ("cvbeb", "jtyjkty"),
    ]
    template = (item[0] for item in entries)
    file = StringIO()
    save_po(file, template, dict(entries))
    file.seek(0)

    result = list(load_po(file))[1:]  # the first entry is metadata
    assert result == [dict(msgid=text, msgstr=translation) for text, translation in entries]


def test_po_reader():
    po_content = """msgid ""
        msgstr ""
        "Project-Id-Version: Dwarf Fortress\\n"
        "PO-Revision-Date: 2019-11-20 10:25+0000\\n"
        "Content-Type: text/plain; charset=UTF-8\\n"
        "Content-Transfer-Encoding: 8bit\\n"
        "Language: ru\\n"
        """

    file = StringIO(po_content)
    po = PoReader(file)
    assert po.meta == {
        "Project-Id-Version": "Dwarf Fortress",
        "PO-Revision-Date": "2019-11-20 10:25+0000",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
        "Language": "ru",
    }
