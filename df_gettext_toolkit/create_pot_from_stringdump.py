from pathlib import Path

import typer

from df_gettext_toolkit.common import TranslationItem
from df_gettext_toolkit.df_ignore_string_rules import all_ignore_rules, dont_ignore
from df_gettext_toolkit.parse_po import save_pot


def main(
    source_file: typer.FileText,
    destination_file: typer.FileTextWrite,
    no_ignore: bool = False,
):
    template = (line.rstrip("\n") for line in source_file)
    ignore_rules = dont_ignore if no_ignore else all_ignore_rules
    file_name = Path(source_file.name).name
    filtered_lines = (
        TranslationItem(text=line, source_file=file_name, line_number=line_number)
        for line_number, line in enumerate(template, 1)
        if not ignore_rules(line)
    )
    save_pot(destination_file, filtered_lines)


if __name__ == "__main__":
    typer.run(main)
