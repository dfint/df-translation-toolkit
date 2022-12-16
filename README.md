# df-gettext-toolkit

[![Test](https://github.com/dfint/df-gettext-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/dfint/df-gettext-toolkit/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/dfint/df-gettext-toolkit/branch/master/graph/badge.svg?token=JfVwndEDlC)](https://codecov.io/gh/dfint/df-gettext-toolkit)
[![Maintainability](https://api.codeclimate.com/v1/badges/8f5de82303b55de3b930/maintainability)](https://codeclimate.com/github/dfint/df-gettext-toolkit/maintainability)

Toolset to convert text to [gettext](https://en.wikipedia.org/wiki/Gettext) format and aback. Includes minimalistic parsers for .po (text) and .mo (binary) formats.

## Installation:

You need Python 3.8.1 (or higher) and poetry (`pip install poetry`).

Clone or download the repo, then install dependencies it with `poetry install` command

## Usage examples:

```bash
poetry run convert hardcoded_steam.po dict.csv cp1251
```
```bash
poetry run create_pot from_steam_text "./Dwarf Fortress/data/vanilla" ./pot_files/
```
```bash
poetry run create_pot from_string_dump stringdump.txt hardcoded_steam.pot
```
