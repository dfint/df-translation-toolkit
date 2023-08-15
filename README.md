# df-gettext-toolkit

[![Test](https://github.com/dfint/df-gettext-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/dfint/df-gettext-toolkit/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/dfint/df-gettext-toolkit/badge.svg?branch=master)](https://coveralls.io/github/dfint/df-gettext-toolkit?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/8f5de82303b55de3b930/maintainability)](https://codeclimate.com/github/dfint/df-gettext-toolkit/maintainability)

Toolset to convert text to [gettext](https://en.wikipedia.org/wiki/Gettext) format and aback. Includes minimalistic parsers for .po (text) and .mo (binary) formats.

> **Note**  
> There are ready to use csv files for most of languages from transifex: https://github.com/dfint/autobuild

## Installation:

You need Python 3.10 (or higher) and poetry (`pip install poetry`).

Clone or download the repo, then install dependencies it with `poetry install` command

## Usage examples:

```bash
poetry run convert hardcoded_steam.po dfint_dictionary.csv cp1251
```
```bash
poetry run create_pot from_steam_text "./Dwarf Fortress/data/vanilla" ./pot_files/
```
```bash
poetry run create_pot from_string_dump stringdump.txt hardcoded_steam.pot
```
