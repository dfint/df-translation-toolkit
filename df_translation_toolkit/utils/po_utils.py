from collections.abc import Iterable
from dataclasses import dataclass
from typing import BinaryIO

from babel.messages import Catalog
from babel.messages.pofile import write_po


@dataclass
class TranslationItem:
    text: str
    translation: str = ""
    context: str | None = None
    source_file: str | None = None
    line_number: int | None = None
    translator_comment: str | None = None  # "#"
    extracted_comment: str | None = None  # "#."
    # reference: Optional[str] = None  # "#: source_file: line_number
    flag: str | None = None  # "#,"
    previous_untranslated_msgid: str | None = None  # "#|"

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
        catalog.add(item.text, context=item.context, locations=[(item.source_file, item.line_number)])

    po_file.write(_default_header + b"\n\n")
    write_po(po_file, catalog, omit_header=True)
