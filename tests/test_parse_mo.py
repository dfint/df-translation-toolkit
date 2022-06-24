import io

import pytest

from df_gettext_toolkit.common import TranslationItem
from df_gettext_toolkit.parse_mo import create_mo, load_mo


def test_load_mo():
    d = [
        TranslationItem("Word1", "Translation1"),
        TranslationItem("Word2", "Translation2"),
        TranslationItem("LongWord", "LongTranslation", context="context"),
    ]
    mo_file = create_mo(d)
    assert list(load_mo(mo_file)) == d


def test_wrong_mo_signature():
    file = io.BytesIO(b"foobar")
    with pytest.raises(ValueError):
        next(load_mo(file))
