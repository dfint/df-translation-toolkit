import typer

from .common import TranslationItem
from .df_ignore_string_rules import all_ignore_rules, dont_ignore
from .parse_po import save_pot


def main(
    source_file: typer.FileText,
    destination_file: typer.FileTextWrite = typer.Option(..., encoding="utf-8"),
    no_ignore: bool = False,
):
    template = (line.rstrip("\n") for line in source_file)
    ignore_rules = dont_ignore if no_ignore else all_ignore_rules
    filtered_lines = (TranslationItem(text=line) for line in template if not ignore_rules(line))
    save_pot(destination_file, filtered_lines)


if __name__ == "__main__":
    typer.run(main)
