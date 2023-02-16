# `python -m df_gettext_toolkit`

**Usage**:

```console
$ python -m df_gettext_toolkit [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `convert`
* `create_pot`

## `python -m df_gettext_toolkit convert`

**Usage**:

```console
$ python -m df_gettext_toolkit convert [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `po_to_csv`: Convert a po file into a csv file in a...

### `python -m df_gettext_toolkit convert po_to_csv`

Convert a po file into a csv file in a specified encoding

**Usage**:

```console
$ python -m df_gettext_toolkit convert po_to_csv [OPTIONS] PO_FILE CSV_FILE ENCODING
```

**Arguments**:

* `PO_FILE`: [required]
* `CSV_FILE`: [required]
* `ENCODING`: [required]

**Options**:

* `--help`: Show this message and exit.

## `python -m df_gettext_toolkit create_pot`

**Usage**:

```console
$ python -m df_gettext_toolkit create_pot [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `from_steam_text`
* `from_string_dump`

### `python -m df_gettext_toolkit create_pot from_steam_text`

**Usage**:

```console
$ python -m df_gettext_toolkit create_pot from_steam_text [OPTIONS] VANILLA_PATH DESTINATION_PATH
```

**Arguments**:

* `VANILLA_PATH`: [required]
* `DESTINATION_PATH`: [required]

**Options**:

* `--source-encoding TEXT`: [default: cp437]
* `--help`: Show this message and exit.

### `python -m df_gettext_toolkit create_pot from_string_dump`

**Usage**:

```console
$ python -m df_gettext_toolkit create_pot from_string_dump [OPTIONS] SOURCE_FILE DESTINATION_FILE
```

**Arguments**:

* `SOURCE_FILE`: [required]
* `DESTINATION_FILE`: [required]

**Options**:

* `--no-ignore / --no-no-ignore`: [default: no-no-ignore]
* `--help`: Show this message and exit.

