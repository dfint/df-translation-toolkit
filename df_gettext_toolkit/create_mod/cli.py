import typer

from df_gettext_toolkit.create_mod import from_template
from df_gettext_toolkit.create_mod import template_from_vanilla
from df_gettext_toolkit.create_mod import generate_preview

app = typer.Typer()
app.command(name="from_template")(from_template.main)
app.command(name="template_from_vanilla")(template_from_vanilla.main)
app.command(name="generate_preview")(generate_preview.main)
