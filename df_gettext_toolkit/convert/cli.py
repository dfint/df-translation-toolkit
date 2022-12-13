import typer

from df_gettext_toolkit.convert import po_to_csv

app = typer.Typer()
app.command(name="po_to_csv")(po_to_csv.main)
