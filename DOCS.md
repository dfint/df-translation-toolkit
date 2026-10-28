# CLI commands

The CLI is a separate uv project in the `cli/` directory with its own lockfile and is not included in the built library package. Run commands from the repository root using `uv run --project cli <command>`.

## `convert`

**Usage**:

```console
$ uv run --project cli convert [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `hardcoded_to_csv`
* `objects_to_csv`

### `convert hardcoded_to_csv`

Convert a po file into a csv file in a specified encoding

**Usage**:

```console
$ uv run --project cli convert hardcoded_to_csv [OPTIONS] PO_FILE CSV_FILE ENCODING
```

**Arguments**:

* `PO_FILE`: [required]
* `CSV_FILE`: [required]
* `ENCODING`: [required]

**Options**:

* `--help`: Show this message and exit.

## `create_pot`

**Usage**:

```console
$ uv run --project cli create_pot [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `from_steam_text`
* `from_string_dump`
* `from_lua`
* `from_raw_objects`
* `from_speech`

### `create_pot from_steam_text`

**Usage**:

```console
$ uv run --project cli create_pot from_steam_text [OPTIONS] VANILLA_PATH DESTINATION_PATH
```

**Arguments**:

* `VANILLA_PATH`: [required]
* `DESTINATION_PATH`: [required]

**Options**:

* `--source-encoding TEXT`: [default: cp437]
* `--help`: Show this message and exit.

### `create_pot from_string_dump`

**Usage**:

```console
$ uv run --project cli create_pot from_string_dump [OPTIONS] SOURCE_FILE DESTINATION_FILE
```

**Arguments**:

* `SOURCE_FILE`: [required]
* `DESTINATION_FILE`: [required]

**Options**:

* `--no-ignore / --no-no-ignore`: [default: no-no-ignore]
* `--help`: Show this message and exit.

## Other command group

* `translate`: `plain_text` and `raws`

Run `uv run --project cli translate --help` for command options.
