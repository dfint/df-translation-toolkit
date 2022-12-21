import typer

from df_gettext_toolkit.create_mod import batch, from_template, generate_preview, template_from_vanilla

app = typer.Typer()
app.command(name="from_template")(from_template.main)
app.command(name="template_from_vanilla")(template_from_vanilla.main)
app.command(name="generate_preview")(generate_preview.main)
app.command(name="batch")(batch.main)
