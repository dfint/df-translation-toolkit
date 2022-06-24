from dataclasses import dataclass
from typing import Optional


@dataclass
class TranslationItem:
    text: str
    translation: str = ""
    context: Optional[str] = None
    source_file: Optional[str] = None
    line_number: Optional[int] = None

    def __eq__(self, other):
        if isinstance(other, TranslationItem):
            return self.text == other.text and self.translation == other.translation and self.context == other.context
        else:
            return False
