import typer

from df_gettext_toolkit.convert import hardcoded_po_to_csv, objects_po_to_csv

app = typer.Typer()
app.command(name="hardcoded_to_csv")(hardcoded_po_to_csv.main)
app.command(name="objects_to_csv")(objects_po_to_csv.main)
