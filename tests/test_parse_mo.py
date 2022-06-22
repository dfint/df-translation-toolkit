from io import BytesIO
from typing import Mapping, List, Tuple

from df_gettext_toolkit.parse_mo import create_mo, load_mo, MO_MAGIC


def test_load_mo():
    d = {
        "Word1": "Translation1",
        "Word2": "Translation2",
        "LongWord": "LongTranslation"
    }
    mo_file = create_mo(d)
    assert {item['msgid']: item['msgstr'] for item in load_mo(mo_file)} == d
