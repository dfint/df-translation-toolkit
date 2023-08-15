from dataclasses import dataclass
from typing import BinaryIO, Iterable, Optional

from babel.messages import Catalog
from babel.messages.pofile import write_po


@dataclass
class TranslationItem:
    text: str
    translation: str = ""
    context: Optional[str] = None
    source_file: Optional[str] = None
    line_number: Optional[int] = None
    translator_comment: Optional[str] = None  # "#"
    extracted_comment: Optional[str] = None  # "#."
    # reference: Optional[str] = None  # "#: source_file: line_number
    flag: Optional[str] = None  # "#,"
    previous_untranslated_msgid: Optional[str] = None  # "#|"

    def __eq__(self, other):
        return (
            isinstance(other, TranslationItem)
            and self.text == other.text
            and self.translation == other.translation
            and self.context == other.context
        )


_default_header = b"""
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
""".strip()


def save_pot(po_file: BinaryIO, template: Iterable[TranslationItem]):
    catalog = Catalog()

    for item in template:
        catalog.add(item.text, locations=[(item.source_file, item.line_number)])

    po_file.write(_default_header + b"\n\n")
    write_po(po_file, catalog, omit_header=True)
