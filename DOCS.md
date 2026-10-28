# `df-translation-toolkit`

The CLI is a separate uv project in the `cli/` directory with its own lockfile and is not included in the built library package. Run commands from the repository root using `uv run --project cli df-translation-toolkit`.

**Usage**:

```console
$ uv run --project cli df-translation-toolkit [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `convert`
* `create_pot`
* `translate`

## `df-translation-toolkit convert`

**Usage**:

```console
$ uv run --project cli df-translation-toolkit convert [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `hardcoded_to_csv`
* `objects_to_csv`

### `df-translation-toolkit convert hardcoded_to_csv`

Convert a po file into a csv file in a specified encoding

**Usage**:

```console
$ uv run --project cli df-translation-toolkit convert hardcoded_to_csv [OPTIONS] PO_FILE CSV_FILE ENCODING
```

**Arguments**:

* `PO_FILE`: [required]
* `CSV_FILE`: [required]
* `ENCODING`: [required]

**Options**:

* `--help`: Show this message and exit.

## `df-translation-toolkit create_pot`

**Usage**:

```console
$ uv run --project cli df-translation-toolkit create_pot [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `from_steam_text`
* `from_string_dump`
* `from_lua`
* `from_raw_objects`
* `from_speech`

### `df-translation-toolkit create_pot from_steam_text`

**Usage**:

```console
$ uv run --project cli df-translation-toolkit create_pot from_steam_text [OPTIONS] VANILLA_PATH DESTINATION_PATH
```

**Arguments**:

* `VANILLA_PATH`: [required]
* `DESTINATION_PATH`: [required]

**Options**:

* `--source-encoding TEXT`: [default: cp437]
* `--help`: Show this message and exit.

### `df-translation-toolkit create_pot from_string_dump`

**Usage**:

```console
$ uv run --project cli df-translation-toolkit create_pot from_string_dump [OPTIONS] SOURCE_FILE DESTINATION_FILE
```

**Arguments**:

* `SOURCE_FILE`: [required]
* `DESTINATION_FILE`: [required]

**Options**:

* `--no-ignore / --no-no-ignore`: [default: no-no-ignore]
* `--help`: Show this message and exit.

## Other command group

* `translate`: `plain_text` and `raws`

Run `uv run --project cli df-translation-toolkit translate --help` for command options.
