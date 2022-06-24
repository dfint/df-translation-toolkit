import io
from io import StringIO
from typing import List, Tuple

from base.base import strip_margin

from df_gettext_toolkit.parse_po import (
    PoReader,
    escape_string,
    load_po,
    parse_metadata,
    parse_metadata_string,
    save_po,
    strip_once,
    unescape_string,
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
    data = strip_margin(
        """
        |# Some comment
        |#: body_default.txt:7
        |msgctxt "BODY:BASIC_1PARTBODY"
        |msgid "[BP:UB:body:bodies]"
        |msgstr "[BP:UB:тело:тела]"
    """
    )

    expected = {
        "#": "Some comment\n",
        "#:": "body_default.txt:7",
        "msgctxt": "BODY:BASIC_1PARTBODY",
        "msgid": "[BP:UB:body:bodies]",
        "msgstr": "[BP:UB:тело:тела]",
    }

    result = next(load_po(StringIO(data)))
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


def test_parse_metadata_string():
    metadata_string = "Content-Type: text/plain; charset=UTF-8\n" "Content-Transfer-Encoding: 8bit\n"
    assert parse_metadata_string(metadata_string) == {
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
    }


def test_parse_metadata():
    header = strip_margin(
        r"""
        |msgid ""
        |msgstr ""
        |"Content-Type: text/plain; charset=UTF-8\n"
        |"Content-Transfer-Encoding: 8bit\n"
    """
    ).strip()

    metadata = next(load_po(io.StringIO(header)))
    assert parse_metadata(metadata) == {
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
    }


def test_po_reader():
    po_content = strip_margin(
        r"""
        |msgid ""
        |msgstr ""
        |"Project-Id-Version: Dwarf Fortress\n"
        |"PO-Revision-Date: 2019-11-20 10:25+0000\n"
        |"Content-Type: text/plain; charset=UTF-8\n"
        |"Content-Transfer-Encoding: 8bit\n"
        |"Language: ru\n"
        |
        |# Some comment
        |#: body_default.txt:7
        |msgctxt "BODY:BASIC_1PARTBODY"
        |msgid "[BP:UB:body:bodies]"
        |msgstr "[BP:UB:тело:тела]"
    """
    )

    po = PoReader(StringIO(po_content))
    assert po.meta == {
        "Project-Id-Version": "Dwarf Fortress",
        "PO-Revision-Date": "2019-11-20 10:25+0000",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
        "Language": "ru",
    }

    assert next(po) == {
        "#": "Some comment\n",
        "#:": "body_default.txt:7",
        "msgctxt": "BODY:BASIC_1PARTBODY",
        "msgid": "[BP:UB:body:bodies]",
        "msgstr": "[BP:UB:тело:тела]",
    }
