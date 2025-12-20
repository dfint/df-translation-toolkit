# df-translation-toolkit

[![Test](https://github.com/dfint/df-translation-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/dfint/df-translation-toolkit/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/dfint/df-translation-toolkit/badge.svg?branch=master)](https://coveralls.io/github/dfint/df-translation-toolkit?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/8f5de82303b55de3b930/maintainability)](https://codeclimate.com/github/dfint/df-translation-toolkit/maintainability)

Toolset to convert text from DF between different formats and prepare it for use in the game

> **Note**  
> There are ready to use csv files for most of languages from transifex: <https://github.com/dfint/autobuild>

## Installation

You need Python 3.10 (or higher) and uv (`pipx install uv`).

Clone or download the repo, then install dependencies with `uv sync` command (optional, they will be installed automatically on a command run).

## Usage examples

```bash
uv run convert hardcoded_steam.po dfint_dictionary.csv cp1251
```

```bash
uv run create_pot from_steam_text "./Dwarf Fortress/data/vanilla" ./pot_files/
```

```bash
uv run create_pot from_string_dump stringdump.txt hardcoded_steam.pot
```
