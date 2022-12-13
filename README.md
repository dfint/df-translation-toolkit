# df-gettext-toolkit

[![Test](https://github.com/dfint/df-gettext-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/dfint/df-gettext-toolkit/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/dfint/df-gettext-toolkit/branch/master/graph/badge.svg?token=JfVwndEDlC)](https://codecov.io/gh/dfint/df-gettext-toolkit)
[![Maintainability](https://api.codeclimate.com/v1/badges/8f5de82303b55de3b930/maintainability)](https://codeclimate.com/github/dfint/df-gettext-toolkit/maintainability)

Toolset to convert text to [gettext](https://en.wikipedia.org/wiki/Gettext) format and aback. Includes minimalistic parsers for .po (text) and .mo (binary) formats.

Usage examples:

```bash
# These commands do the same thing: convert a po file into a csv file in a specified encoding
poetry run python -m df_gettext_toolkit convert po_to_csv file.po result.csv cp1251
poetry run df_gettext_toolkit convert po_to_csv file.po result.csv cp1251
poetry run convert file.po result.csv cp1251
```