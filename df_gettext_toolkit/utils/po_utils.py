from dataclasses import dataclass
from typing import Optional, TextIO, Iterator

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
        if isinstance(other, TranslationItem):
            return self.text == other.text and self.translation == other.translation and self.context == other.context
        else:
            return False


def save_pot(po_file: TextIO, template: Iterator[TranslationItem]):
    catalog = Catalog()

    for item in template:
        catalog.add(item.text, locations=[(item.source_file, item.line_number)])

    write_po(po_file, catalog)
