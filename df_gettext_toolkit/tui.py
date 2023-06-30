import click
import typer
from trogon import tui

from df_gettext_toolkit.cli import commands


@tui()
@click.group()
def cli():
    pass


for command in commands:
    typer_click_object = typer.main.get_command(command[1])
    cli.add_command(typer_click_object, command[0])

if __name__ == '__main__':
    cli()
