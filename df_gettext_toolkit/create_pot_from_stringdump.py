import typer

from .df_ignore_string_rules import all_ignore_rules
from .po import save_pot


def main(source_file: str, destination_file: str, no_ignore=False):
    with open(source_file) as string_dump:
        template = (line.rstrip('\n') for line in string_dump)
        ignore_rules = (lambda s: False) if no_ignore else all_ignore_rules
        filtered_lines = (line for line in template if not ignore_rules(line))
        with open(destination_file, 'w', encoding='utf-8') as pot_file:
            save_pot(pot_file, filtered_lines)


if __name__ == '__main__':
    typer.run(main)
