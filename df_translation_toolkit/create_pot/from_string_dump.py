import typer

from df_translation_toolkit.utils.df_ignore_string_rules import all_ignore_rules, dont_ignore
from df_translation_toolkit.utils.po_utils import TranslationItem, save_pot


def main(
    source_file: typer.FileText,
    destination_file: typer.FileBinaryWrite,
    no_ignore: bool = False,
):
    template = (line.rstrip("\n") for line in source_file)
    ignore_rules = dont_ignore if no_ignore else all_ignore_rules
    filtered_lines = (
        TranslationItem(text=line)
        for line in template
        if not ignore_rules(line)
    )
    save_pot(destination_file, filtered_lines)


if __name__ == "__main__":
    typer.run(main)
