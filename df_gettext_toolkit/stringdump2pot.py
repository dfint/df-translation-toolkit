import click

from .po import save_pot
from .df_ignore_string_rules import ignore_all


@click.command()
@click.argument('source_file')
@click.argument('destination_file')
@click.option('--no-ignore', default=False)
def main(source_file, destination_file, no_ignore=False):
    with open(source_file) as stringdump:
        template = (line.rstrip('\n') for line in stringdump)
        ignore_rules = (lambda s: False) if no_ignore else ignore_all
        filtered_lines = (line for line in template if not ignore_rules(line))
        with open(destination_file, 'w', encoding='utf-8') as potfile:
            save_pot(potfile, filtered_lines)


if __name__ == '__main__':
    main()
