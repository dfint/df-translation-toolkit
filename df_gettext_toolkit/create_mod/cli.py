import typer

from df_gettext_toolkit.create_mod import from_vanilla
from df_gettext_toolkit.create_mod import template_from_vanilla

app = typer.Typer()
app.command(name="from_vanilla")(from_vanilla.main)
app.command(name="template_from_vanilla")(template_from_vanilla.main)
