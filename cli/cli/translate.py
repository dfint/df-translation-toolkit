import typer

from df_translation_toolkit.translate import translate_plain_text, translate_raws

app = typer.Typer()
app.command(name="plain_text")(translate_plain_text.main)
app.command(name="raws")(translate_raws.main)
